"""Run a critic over every (condition, item, sample) and append verdicts to a JSONL file.

Three backends:
  openai     any OpenAI-compatible server: Ollama or LM Studio on your Mac, vLLM on your
             PC or HPC, or a hosted API.
  anthropic  the Claude API through the official `anthropic` SDK, with a dollar cap
             (--max-usd) and an optional Message Batches mode (--batch, half price).
  sim        a simulated critic with known parameters (tests the pipeline end to end).
Re-running the same command resumes where it left off; finished trials are skipped.

Examples:
    # simulated critic, no model needed
    uv run python -m pilot.run --backend sim --model sim-critic

    # Ollama on the Mac
    uv run python -m pilot.run --model qwen3.5:9b --base-url http://localhost:11434/v1

    # vLLM (PC or HPC node), thinking disabled for Qwen-style chat templates
    uv run python -m pilot.run --model Qwen/Qwen3.5-9B --base-url http://localhost:8000/v1 \\
        --concurrency 64 --extra-body '{"chat_template_kwargs": {"enable_thinking": false}}'

    # Claude Sonnet 5.5, thinking off, at most $0.50 (the key comes from Keychain)
    scripts/with_key.sh .venv/bin/python -m pilot.run --backend anthropic --model claude-sonnet-5-5 \\
        --thinking off --label sonnet-5.5-nothink --max-usd 0.50

Claude API notes: temperature is not sent (the Claude 5.5 models reject sampling
parameters), so Claude trials are sampled at the API default. There are no logprobs;
the ROC uses the verbalized p_error. Refusals are logged (verdict None, refusal_category
set) and never retried on another model.
"""
import argparse
import ast
import asyncio
import json
import math
import os
import re
import time
from collections import Counter
from pathlib import Path

from .prompts import build_messages, resolve_conditions
from .simulate import SimulatedCritic

ROOT = Path(__file__).resolve().parent.parent
THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
JSON_RE = re.compile(r"\{[^{}]*\}")
# Verdict words of both answer formats (prompts.USER_TEMPLATE and the label-swap control).
VERDICT_WORDS = {"error": "error", "correct": "correct", "flawed": "error", "sound": "correct"}


def token_verdict(token: str) -> str | None:
    """Verdict a token starts, e.g. "err", "Correct" or "fl" (of "flawed"); None for anything else."""
    w = token.strip(' "\'').lower()
    if len(w) < 2:
        return None
    return next((v for word, v in VERDICT_WORDS.items() if word.startswith(w) or w.startswith(word)), None)

# USD per million tokens (input, output) on the standard Claude API; batches cost half.
# Thinking tokens are billed as output. Checked against the pricing page on 2026-11-07.
# Haiku 5.5's rate is for prompts of 100K tokens or fewer (every prompt here is under 10K).
PRICES = {
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-fable-5-1": (10.00, 50.00),
    # OpenAI, standard rate; Flex costs half. Reasoning tokens are billed as output. Read from the pricing page on 2026-11-10.
    "gpt-6.1-sol": (2.00, 10.00),
    "gpt-6-luna": (0.10, 0.50),
}
# How each model turns extended thinking off. Opus 5.5 and Fable 5.1 always think.
THINKING_OFF = {"claude-sonnet-5-5": {"type": "between_tools"}, "claude-haiku-5-5": {"type": "disabled"}}
SPEND_LEDGER = ROOT / "results" / "api_spend.jsonl"


def parse_response(text: str | None) -> tuple[str | None, int | None]:
    """Pull (verdict, p_error) out of a reply; (None, None) if it can't be parsed."""
    if not text:
        return None, None
    text = THINK_RE.sub("", text)
    for blob in reversed(JSON_RE.findall(text)):
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            # Small models sometimes answer with a Python dict ({'verdict': 'error', ...}).
            try:
                obj = ast.literal_eval(blob)
            except (ValueError, SyntaxError):
                continue
        if not isinstance(obj, dict):
            continue
        verdict = VERDICT_WORDS.get(str(obj.get("verdict", "")).strip().lower())
        if verdict is None:
            continue
        p = obj.get("p_error", obj.get("p_flawed"))
        try:
            p = min(100, max(0, int(round(float(p)))))
        except (TypeError, ValueError):
            p = None
        return verdict, p
    return None, None


def verdict_logprob_score(content_logprobs) -> float | None:
    """P(error) from the verdict token's top alternatives: mass on "error" / (mass on "error" + "correct").

    Gives a continuous score at temperature 0, which verbalized p_error often doesn't
    (small models tend to answer only 0 or 100). Only meaningful with thinking off.
    """
    if not content_logprobs:
        return None
    text = ""
    starts = []
    for t in content_logprobs:
        starts.append(len(text))
        text += t.token
    # The last "verdict" is the answer; reasoning text before it may use the same word.
    key = text.rfind("verdict")
    if key < 0:
        return None
    for i, t in enumerate(content_logprobs):
        if starts[i] < key + len("verdict") or token_verdict(t.token) is None:
            continue
        alts = {a.token: a.logprob for a in (t.top_logprobs or [])}
        alts.setdefault(t.token, t.logprob)
        mass = {"error": 0.0, "correct": 0.0}
        for tok, lp in alts.items():
            if (v := token_verdict(tok)) is not None:
                mass[v] += math.exp(lp)
        total = mass["error"] + mass["correct"]
        return mass["error"] / total if total > 0 else None
    return None


def slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model)


def load_done(path: Path) -> set[tuple]:
    done = set()
    if path.exists():
        for line in path.open():
            r = json.loads(line)
            if r.get("verdict") is not None or not r.get("retryable", False):
                done.add((r["condition"], r["item_id"], r["sample"]))
    return done


# ---------------------------------------------------------------- OpenAI-compatible

async def call_openai(client, args, messages, sample) -> dict:
    if args.effort:
        # OpenAI reasoning models: no sampling parameters, and the reply limit also covers the reasoning tokens.
        kwargs = dict(model=args.model, messages=messages, reasoning_effort=args.effort, max_completion_tokens=args.max_tokens)
        if args.flex:
            kwargs["service_tier"] = "flex"
    else:
        kwargs = dict(model=args.model, messages=messages, temperature=args.temperature, max_tokens=args.max_tokens)
        if args.temperature > 0:
            kwargs["seed"] = sample
    if args.extra_body:
        kwargs["extra_body"] = json.loads(args.extra_body)
    if args.logprobs:
        kwargs.update(logprobs=True, top_logprobs=10)
    resp = await client.chat.completions.create(**kwargs)
    choice = resp.choices[0]
    usage = resp.usage
    lp = verdict_logprob_score(choice.logprobs.content if choice.logprobs else None) if args.logprobs else None
    # vLLM with --reasoning-parser returns the thinking separately from the answer.
    msg = choice.message
    reasoning = getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", None)
    rec = dict(raw=msg.content, reasoning=reasoning, finish_reason=choice.finish_reason,
               prompt_tokens=usage.prompt_tokens if usage else None,
               completion_tokens=usage.completion_tokens if usage else None, p_error_lp=lp)
    if args.max_usd is not None:
        # Priced by the tier the reply says it was served on, so a request that was not served as Flex counts in full.
        tier = getattr(resp, "service_tier", None)
        details = getattr(usage, "completion_tokens_details", None)
        rec.update(cost_usd=round(usd(args.model, usage.prompt_tokens, usage.completion_tokens, batch=tier == "flex"), 6),
                   service_tier=tier, reasoning_tokens=getattr(details, "reasoning_tokens", None), api_model=resp.model)
    return rec


# ---------------------------------------------------------------- Claude API

def usd(model: str, input_tokens: int, output_tokens: int, batch: bool) -> float:
    pin, pout = PRICES[model]
    return (input_tokens * pin + output_tokens * pout) / 1e6 * (0.5 if batch else 1.0)


def anthropic_params(args, messages) -> dict:
    """Messages API request for one trial. No temperature/top_p/top_k: these models reject them."""
    params = dict(model=args.model, max_tokens=args.max_tokens, system=messages[0]["content"],
                  messages=[{"role": "user", "content": messages[1]["content"]}])
    if args.thinking == "off":
        # No extended thinking: `between_tools` on Sonnet 5.5 (`disabled` is a 400 there), `disabled` on Haiku 5.5.
        params["thinking"] = dict(THINKING_OFF[args.model])
    else:
        # Summarized thinking text is returned so the reasoning can be read; billing is the same.
        params["thinking"] = {"type": "adaptive", "display": "summarized"}
    if args.effort:
        params["output_config"] = {"effort": args.effort}
    return params


def read_message(msg, model: str, batch: bool) -> dict:
    text = "".join(b.text for b in msg.content if b.type == "text")
    thinking = "\n\n".join(b.thinking for b in msg.content if b.type == "thinking" and getattr(b, "thinking", None))
    u = msg.usage
    rec = dict(raw=text or None, reasoning=thinking or None, finish_reason=msg.stop_reason,
               prompt_tokens=u.input_tokens, completion_tokens=u.output_tokens, p_error_lp=None,
               cost_usd=round(usd(model, u.input_tokens, u.output_tokens, batch), 6), api_model=msg.model)
    if msg.stop_reason == "refusal":
        sd = getattr(msg, "stop_details", None)
        rec["refusal_category"] = getattr(sd, "category", None) if sd else None
    return rec


def check_anthropic_args(args):
    if args.model not in PRICES:
        raise SystemExit(f"no price for {args.model}; add it to PRICES in pilot/run.py ({list(PRICES)})")
    if args.thinking is None:
        raise SystemExit("--backend anthropic needs --thinking off|on")
    if args.thinking == "off" and args.model not in THINKING_OFF:
        raise SystemExit(f"thinking can't be turned off on {args.model}; only on {list(THINKING_OFF)}")
    if args.thinking == "off" and args.effort in ("xhigh", "max"):
        raise SystemExit("thinking off needs --effort high or lower")
    if args.batch_chunk is not None and args.batch_chunk < 1:
        raise SystemExit("--batch-chunk must be at least 1")
    if args.max_usd is None:
        raise SystemExit("--backend anthropic needs a spending cap: --max-usd <dollars>")
    if args.temperature:
        print("note: --temperature is ignored for the Claude API (sampling parameters are rejected)")


def log_spend(label, args, mode, n, tin, tout, cost):
    global SPEND_LEDGER
    if args.backend != "anthropic":   # a separate ledger, so api_spend.jsonl stays the Claude credit
        SPEND_LEDGER = SPEND_LEDGER.with_name("openai_spend.jsonl")
    SPEND_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with SPEND_LEDGER.open("a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "label": label, "model": args.model,
                            "thinking": args.thinking, "mode": mode, "calls": n, "input_tokens": tin,
                            "output_tokens": tout, "usd": round(cost, 4)}) + "\n")
    total = sum(json.loads(l)["usd"] for l in SPEND_LEDGER.open())
    print(f"spent ${cost:.4f} this run ({n} calls, {tin} in / {tout} out tokens); "
          f"${total:.2f} total in {SPEND_LEDGER.relative_to(ROOT) if SPEND_LEDGER.is_relative_to(ROOT) else SPEND_LEDGER}")


def est_input_tokens(messages) -> int:
    return int(sum(len(m["content"]) for m in messages) / 3.0) + 20  # conservative: ~3 chars/token


def batch_estimate(args, part, spent):
    """(expected, worst, basis) in USD for one chunk of trials sent as a batch."""
    pin, pout = PRICES[args.model]
    tin = sum(est_input_tokens(build_messages(it, c)) for c, it, s in part)
    worst = (tin * pin + len(part) * args.max_tokens * pout) / 1e6 * 0.5
    if spent["n"] >= 50:  # after a finished chunk, use what calls actually cost, with 20% headroom
        per = spent["usd"] / spent["n"]
        return 1.2 * per * len(part), worst, f"measured ${per:.4f}/call + 20%"
    exp_out = args.est_output_tokens or (100 if args.thinking == "off" else args.max_tokens // 4)
    return (tin * pin + len(part) * exp_out * pout) / 1e6 * 0.5, worst, f"~{exp_out} output tokens each"


def collect_batch(client, args, state, state_path, out, done, has_error, label, spent):
    """Wait for a submitted batch, append its results to `out`, log the spend. Returns the trial keys seen."""
    t0 = time.time()
    while True:
        b = client.messages.batches.retrieve(state["batch_id"])
        if b.processing_status == "ended":
            break
        rc = b.request_counts
        print(f"  {time.time() - t0:5.0f}s  {b.processing_status}: {rc.processing} processing, "
              f"{rc.succeeded} succeeded, {rc.errored} errored")
        time.sleep(args.poll)
    seen = set()
    n = tin = tout = 0
    cost = 0.0
    with out.open("a") as f:
        for res in client.messages.batches.results(state["batch_id"]):
            c, iid, s = state["mapping"][res.custom_id]
            seen.add((c, iid, s))
            if (c, iid, s) in done:  # already written by an earlier, interrupted pass over this batch
                continue
            record = {"model": label, "condition": c, "item_id": iid, "sample": s, "has_error": has_error[iid],
                      "batch_id": state["batch_id"]}
            if res.result.type == "succeeded":
                rec = read_message(res.result.message, args.model, batch=True)
                verdict, p_error = (None, None) if rec["finish_reason"] == "refusal" else parse_response(rec["raw"])
                record.update(verdict=verdict, p_error=p_error, retryable=False, **rec)
                n += 1
                tin += rec["prompt_tokens"]
                tout += rec["completion_tokens"]
                cost += rec["cost_usd"]
                done.add((c, iid, s))
            else:
                err = getattr(res.result, "error", None)
                record.update(verdict=None, p_error=None, retryable=True,
                              error=f"batch {res.result.type}: {getattr(getattr(err, 'error', err), 'type', '')}")
            f.write(json.dumps(record) + "\n")
    state_path.rename(state_path.with_name(f"{out.stem}.batch.{state['batch_id']}.done.json"))
    log_spend(label, args, "batch", n, tin, tout, cost)
    spent["usd"] += cost
    spent["n"] += n
    return seen


def run_batch(args, todo, done, out, label):
    """Send pending trials as Message Batches (half price), wait, and write the results.

    --batch-chunk N splits the trials into batches of N, sent one after another. The whole
    run's estimate is checked against --max-usd before anything is sent; before each later
    chunk the check is repeated with the measured cost per call, so a run whose replies turn
    out longer than expected stops after at most one chunk over the estimate. A batch can't
    be stopped part-way, so the chunk size bounds the overrun.

    The pending batch id is saved next to the output file, so an interrupted run picks the
    same batch back up instead of paying twice.
    """
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    has_error = {it["id"]: it["has_error"] for it in map(json.loads, Path(args.items).open())}
    spent = {"usd": 0.0, "n": 0}
    state_path = out.with_name(out.stem + ".batch.json")
    client = None if args.dry_run else anthropic.Anthropic(max_retries=3)
    if state_path.exists():
        if args.dry_run:
            raise SystemExit(f"a batch is pending in {state_path.name}; run without --dry-run to collect it first")
        state = json.loads(state_path.read_text())
        print(f"picking up batch {state['batch_id']} from {state_path.name}")
        seen = collect_batch(client, args, state, state_path, out, done, has_error, label, spent)
        todo = [t for t in todo if (t[0], t[1]["id"], t[2]) not in seen]
        if not todo:
            return
    size = args.batch_chunk or len(todo)
    chunks = [todo[k:k + size] for k in range(0, len(todo), size)]
    expected, worst, basis = batch_estimate(args, todo, spent)
    print(f"{len(todo)} trials in {len(chunks)} batch(es) of up to {size}: estimated ${expected:.2f} ({basis}), "
          f"worst case ${worst:.2f} if every reply used all {args.max_tokens} tokens; cap ${args.max_usd:.2f}")
    if spent["usd"] + expected > args.max_usd:
        raise SystemExit(f"estimate ${spent['usd'] + expected:.2f} is over --max-usd {args.max_usd}; not submitting")
    for k, part in enumerate(chunks):
        if k > 0:
            expected, _, basis = batch_estimate(args, part, spent)
            if spent["usd"] + expected > args.max_usd:
                left = sum(map(len, chunks[k:]))
                print(f"cost cap: ${spent['usd']:.2f} spent, next batch estimated ${expected:.2f} ({basis}); "
                      f"stopping with {left} trials not sent (re-run with a higher --max-usd to resume)")
                return
        mapping, reqs = {}, []
        for j, (c, it, s) in enumerate(part):
            cid = f"t{j}"
            mapping[cid] = [c, it["id"], s]
            reqs.append(Request(custom_id=cid, params=MessageCreateParamsNonStreaming(
                **anthropic_params(args, build_messages(it, c)))))
        if args.dry_run:
            first = dict(reqs[0]["params"])
            first["messages"] = f"<user message, {len(first['messages'][0]['content'])} chars>"
            first["system"] = first["system"][-90:]
            print(f"dry run: {len(todo)} requests in {len(chunks)} batch(es), nothing sent. First: "
                  f"{reqs[0]['custom_id']} {mapping[reqs[0]['custom_id']]} {json.dumps(first)}")
            print("conditions:", dict(sorted(Counter(c for c, _, _ in todo).items())))
            return
        batch = client.messages.batches.create(requests=reqs)
        state = {"batch_id": batch.id, "label": label, "mapping": mapping}
        state_path.write_text(json.dumps(state))
        print(f"submitted batch {k + 1}/{len(chunks)}: {batch.id} ({len(reqs)} requests)")
        collect_batch(client, args, state, state_path, out, done, has_error, label, spent)
    if len(chunks) > 1:
        print(f"all {len(chunks)} batches done: ${spent['usd']:.2f} for {spent['n']} calls")


# ---------------------------------------------------------------- main loop

async def main_async(args):
    items = [json.loads(l) for l in Path(args.items).open()]
    if args.limit:
        # Keep the class balance when trimming: take the first N of each class.
        correct = [it for it in items if not it["has_error"]][: args.limit // 2]
        flawed = [it for it in items if it["has_error"]][: args.limit - args.limit // 2]
        items = correct + flawed
    conditions = resolve_conditions(args.conditions)
    label = args.label or args.model
    out = Path(args.out or ROOT / "results" / f"{slug(label)}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    done = load_done(out)
    todo = [(c, it, s) for c in conditions for it in items for s in range(args.samples)
            if (c, it["id"], s) not in done]
    print(f"{label}: {len(conditions)} conditions x {len(items)} items x {args.samples} samples; "
          f"{len(todo)} to run, {len(done)} already in {out}")
    if args.backend == "anthropic":
        check_anthropic_args(args)
    elif args.max_usd is not None and args.model not in PRICES:
        raise SystemExit(f"no price for {args.model}; add it to PRICES in pilot/run.py to use --max-usd")
    if not todo:
        return
    if args.backend == "anthropic" and args.batch:
        return run_batch(args, todo, done, out, label)

    spend = {"usd": 0.0, "reserved": 0.0, "n": 0, "in": 0, "out": 0, "stopped": False, "fatal": None}
    if args.backend == "sim":
        sim = SimulatedCritic(seed=args.sim_seed, claim_shift=json.loads(args.sim_claim_shift or "{}"))
        async def call(messages, item, condition, sample):
            return dict(raw=sim.respond(item, condition), finish_reason="stop")
    elif args.backend == "anthropic":
        import anthropic
        client = anthropic.AsyncAnthropic(timeout=args.timeout, max_retries=2)
        shown_limits = False
        async def call(messages, item, condition, sample):
            nonlocal shown_limits
            async with client.messages.stream(**anthropic_params(args, messages)) as stream:
                msg = await stream.get_final_message()
                if not shown_limits:
                    shown_limits = True
                    h = stream.response.headers
                    lim = {k.replace("anthropic-ratelimit-", ""): v for k, v in h.items()
                           if k.startswith("anthropic-ratelimit-") and k.endswith("-limit")}
                    print(f"  rate limits: {lim}")
            return read_message(msg, args.model, batch=False)
    else:
        from openai import AsyncOpenAI
        api_key = os.environ.get(args.api_key_env, "") if args.api_key_env else "EMPTY"
        client = AsyncOpenAI(base_url=args.base_url, api_key=api_key or "EMPTY", timeout=args.timeout, max_retries=0)
        async def call(messages, item, condition, sample):
            return await call_openai(client, args, messages, sample)

    async def reserve(messages) -> float | None:
        """Cost guard: hold back an estimate for this call, or None if it would pass --max-usd.

        While calls in flight hold the room, wait for them; stop only when what has
        actually been spent leaves no room for one more call.
        """
        if args.max_usd is None:
            return 0.0
        pin, pout = PRICES[args.model]
        while True:
            if spend["stopped"] or spend["fatal"]:
                return None
            if spend["n"] >= 3:   # mean of finished calls, with headroom
                est = 1.5 * spend["usd"] / spend["n"]
            else:                 # before that, assume the reply uses all of max_tokens
                est = (est_input_tokens(messages) * pin + args.max_tokens * pout) / 1e6
            if spend["usd"] + est > args.max_usd:
                print(f"  cost cap: ${spend['usd']:.3f} spent; not starting more calls (--max-usd {args.max_usd})")
                spend["stopped"] = True
                return None
            if spend["usd"] + spend["reserved"] + est <= args.max_usd:
                spend["reserved"] += est
                return est
            await asyncio.sleep(0.5)

    sem = asyncio.Semaphore(args.concurrency)
    n_done = n_fail = n_cut = n_refused = 0
    t0 = time.time()

    with out.open("a") as f:
        async def one(condition, item, sample):
            nonlocal n_done, n_fail, n_cut, n_refused
            async with sem:
                messages = build_messages(item, condition)
                held = await reserve(messages)
                if held is None:
                    return
                record = {"model": label, "condition": condition, "item_id": item["id"],
                          "sample": sample, "has_error": item["has_error"]}
                for attempt in range(args.retries + 1):
                    try:
                        t = time.time()
                        rec = await call(messages, item, condition, sample)
                        refused = rec.get("finish_reason") == "refusal"
                        verdict, p_error = (None, None) if refused else parse_response(rec.get("raw"))
                        record.update(verdict=verdict, p_error=p_error, latency_s=round(time.time() - t, 2),
                                      retryable=False, **rec)
                        if not record.get("reasoning"):
                            record.pop("reasoning", None)
                        record.pop("error", None)
                        break
                    except Exception as e:  # network errors, rate limits, server restarts
                        record.update(verdict=None, p_error=None, error=f"{type(e).__name__}: {e}", retryable=True)
                        status = getattr(e, "status_code", None)
                        if status in (400, 401, 403, 404, 413):  # our request is wrong: stop, don't retry
                            spend["fatal"] = record["error"]
                            break
                        await asyncio.sleep(min(60, 2 ** attempt))
                spend["reserved"] -= held
                if record.get("cost_usd") is not None:
                    spend["usd"] += record["cost_usd"]
                    spend["n"] += 1
                    spend["in"] += record["prompt_tokens"]
                    spend["out"] += record["completion_tokens"]
                f.write(json.dumps(record) + "\n")
                f.flush()
                n_done += 1
                n_fail += record["verdict"] is None
                n_cut += record.get("finish_reason") in ("length", "max_tokens")
                n_refused += record.get("finish_reason") == "refusal"
                if n_done % args.log_every == 0 or n_done == len(todo):
                    rate = n_done / (time.time() - t0)
                    cost = f", ${spend['usd']:.3f}" if args.max_usd is not None else ""
                    print(f"  {n_done}/{len(todo)} done, {n_fail} unparsed/failed, {rate:.2f}/s{cost}")

        await asyncio.gather(*(one(c, it, s) for c, it, s in todo))
    if args.max_usd is not None and args.backend != "sim":
        log_spend(label, args, "flex" if args.flex else "realtime", spend["n"], spend["in"], spend["out"], spend["usd"])
        if spend["fatal"]:
            print(f"stopped on a request error (fix and re-run to resume): {spend['fatal']}")
        if spend["stopped"]:
            print(f"stopped at the cost cap with {len(todo) - n_done} trials not run; re-run with a higher --max-usd to resume")
        if n_refused:
            print(f"note: {n_refused} replies were refusals (logged with refusal_category, verdict None)")
    if n_cut:
        print(f"warning: {n_cut} replies hit --max-tokens ({args.max_tokens}). The model is probably thinking "
              f"before answering: raise --max-tokens or disable thinking (see README).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="model name as the server knows it")
    ap.add_argument("--label", default=None,
                    help="name used in results and analysis (default: --model); e.g. qwen3.5:9b-nothink")
    ap.add_argument("--backend", choices=["openai", "anthropic", "sim"], default="openai")
    ap.add_argument("--base-url", default="http://localhost:11434/v1", help="OpenAI-compatible endpoint (default: Ollama)")
    ap.add_argument("--api-key-env", default=None, help="name of the env var holding the API key, e.g. OPENROUTER_API_KEY")
    ap.add_argument("--items", default=str(ROOT / "data" / "items.jsonl"))
    ap.add_argument("--conditions", default="base_rate", help="condition names or sets (base_rate, strictness), comma-separated")
    ap.add_argument("--samples", type=int, default=1, help="samples per item and condition")
    ap.add_argument("--temperature", type=float, default=0.0, help="OpenAI-compatible backends only")
    ap.add_argument("--max-tokens", type=int, default=1024, help="raise for reasoning models that think before answering")
    ap.add_argument("--extra-body", default=None, help="JSON merged into the request body, e.g. to disable thinking")
    ap.add_argument("--logprobs", action="store_true",
                    help="also record P(error) from the verdict token's logprobs (thinking off; Ollama, vLLM, OpenAI)")
    ap.add_argument("--thinking", choices=["off", "on"], default=None,
                    help="Claude API: off = no extended thinking (Sonnet 5.5, Haiku 5.5), on = adaptive thinking")
    ap.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"], default=None,
                    help="Claude API output_config.effort (default: the model's own default)")
    ap.add_argument("--max-usd", type=float, default=None,
                    help="stop before spending more than this (required for the Claude API; OpenAI models need a PRICES entry)")
    ap.add_argument("--flex", action="store_true", help="OpenAI: Flex processing (half price, slower; needs --effort)")
    ap.add_argument("--batch", action="store_true", help="Claude API: send trials as Message Batches (half price)")
    ap.add_argument("--batch-chunk", type=int, default=None,
                    help="Claude batch: trials per batch; batches go one after another, with the cost cap re-checked between them")
    ap.add_argument("--est-output-tokens", type=int, default=None,
                    help="Claude batch: expected output tokens per call, for the cost estimate")
    ap.add_argument("--poll", type=float, default=30, help="Claude batch: seconds between status checks")
    ap.add_argument("--dry-run", action="store_true", help="Claude batch: build the batch and print the estimate, send nothing")
    ap.add_argument("--concurrency", type=int, default=4, help="parallel requests; ~2-4 for Ollama, 32-128 for vLLM")
    ap.add_argument("--limit", type=int, default=None, help="only use the first N items (balanced), for smoke tests")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--sim-seed", type=int, default=0)
    ap.add_argument("--sim-claim-shift", default=None, help='sim backend: JSON of true c shifts, e.g. {"presuppose": -0.9}')
    ap.add_argument("--out", default=None, help="output JSONL (default: results/<model>.jsonl)")
    asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    main()
