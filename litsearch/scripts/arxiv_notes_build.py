#!/usr/bin/env python3
"""Build the related-papers section of streams/arxiv_notes.md from streams/arxiv_screening.csv.

Usage: python3 -I arxiv_notes_build.py <litsearch_dir> <out_md_fragment>

Coverage codes per claim (C1-C8), assigned by hand from what was read:
  partly  = same idea on an LLM critic/judge/verifier/monitor, with a different measurement, manipulation or
            a single condition (PROTOCOL.md 'partly covered')
  context = same idea outside critic tasks, or a different manipulation that bears on the claim; does not cover it
  (claims not listed: does not touch)
"""
import csv
import os
import sys

COV = {
    "2412.11009": {"C1": "context: base-rate neglect in Bayesian word problems, not critics", "C2": "context (counterpoint): rewording to 'compute the posterior probability' fixed GPT-4o"},
    "2503.07003": {"C6": "context: general words-vs-deeds gap, no judging task"},
    "2506.21561": {"C8": "context: reasoning models show less truth-bias in veracity judgments (criterion-like), no prior or payoff"},
    "2509.13332": {"C8": "context: thinking vs non-thinking judges (accuracy only)", "C5": "context: small Qwen3 sizes compared on accuracy"},
    "2510.17880": {"C3": "context: stated punishment cost under-used outside critics", "C8": "context: reasoning models more cost-sensitive"},
    "2511.10871": {"C4": "partly: framing (fact vs speaker correctness) and rebuttals shift judge verdicts; accuracy only"},
    "2601.05376": {"C4": "context: persona and bold/cautious style shift clinical risk propensity; not a critic"},
    "2601.19082": {"C3": "context: payoff scale changes cooperation although theory predicts no change", "C4": "context: persona effect reverses with scale"},
    "2602.07996": {"C6": "context: judges' rationales omit the cues that drive verdicts (reverse direction of C6)"},
    "2603.16244": {"C4": "partly: extra review rounds raise recall and false positives (criterion shift), different manipulation"},
    "2603.25112": {"C7": "context: type-2 ROC and z-ROC from token log-probabilities for QA confidence, not critics"},
    "2603.29693": {"C3": "context (counterpoint): GPT-5 shifts SDT c toward the safer answer under stated risk; no magnitudes or optimum", "C7": "context: meta-d' for LLMs"},
    "2604.00228": {"C6": "context: refusal self-prediction vs behaviour with SDT"},
    "2604.03904": {"C3": "context (partial counterpoint): announced abstain payoffs move abstention as expected, an extreme wrong-answer penalty does not"},
    "2604.16790": {"C4": "partly: prompt cues shift code-judge verdicts toward the cued option"},
    "2604.24074": {"C4": "partly: judge-prompt framing shifts harmful-response rates by up to 24 pp; no ground truth"},
    "2604.28031": {"C6": "context: models restate constraints they violate (8-99%)"},
    "2605.05957": {"C6": "context: knowing but not correcting false premises"},
    "2605.06161": {"C4": "partly: strict vs lenient policy wording flips 32-70% of safety-judge verdicts; flips only"},
    "2605.14038": {"C6": "context: probe-decoded tool necessity vs tool calls"},
    "2605.26174": {"C4": "partly: SDT d'/c of a defect-detecting critic under orchestration (not tone)", "C5": "context: c falls across model generations within one developer (not prior use)", "C8": "partly: reasoning on vs off in one model lowers c (1.29 to 0.96) and raises d' (0.42 to 0.66); no prior or payoff"},
    "2605.29087": {"C8": "context: think mode widens a trace-answer gap under pushback", "C6": "context: latent-correct answers not emitted", "C7": "context: answer-slot token probe"},
    "2606.00467": {"C1": "context: added definitions/examples rescue only 34.8% of judge errors (in-context information under-used)", "C2": "context: added instructions have limited corrective power"},
    "2606.06306": {"C5": "context: small instruction-tuned models are more manipulation-sensitive (sycophancy)"},
    "2606.07834": {"C2": "context: a detailed instruction leaves 21-48% overcommitment", "C6": "partly: judges recognise the conflict when asked afterwards but did not act on it (not a stated lean)"},
    "2606.07874": {"C1": "context: safety judges change ~5% of verdicts where new definitions require >15%", "C2": "context: definitions stated in context barely steer judges"},
    "2606.09843": {"C6": "context: self-report barely tracks behaviour (r = .09)"},
    "2606.11016": {"C6": "context: stated decision driver matches behavioural driver 61%", "C8": "context: thinking changes that agreement"},
    "2606.12730": {"C6": "context: self-report/behaviour coherence collapses for context-primed behaviour"},
    "2606.22974": {"C3": "context: offering high-utility incentives does nothing while exhortation works (generation, not judging)", "C4": "context: exhortation and role lines move quality"},
    "2607.02575": {"C1": "context: context-specified decision criteria under-used ('rigid boundary bias')", "C5": "context: 7B to 32B barely changes criterion sensitivity"},
    "2607.05904": {"C4": "context: judge protocol (commit own answer first) cuts false positives"},
    "2607.10411": {"C4": "partly: false-premise framings flip code-smell critic decisions (flip rates)"},
    "2607.13618": {"C6": "context: knowing-doing gap in a POMDP", "C1": "context: agents scored against an exact Bayes-filter (ideal) oracle"},
    "2608.04415": {"C4": "partly: peer-asserted labels raise safety-judge false alarms 56% to 88% with misses nearly flat", "C5": "context: Qwen 7B far more pliable than 32B"},
    "2608.08975": {"C4": "partly: strict review protocol lowers AI-reviewer scores 1.36 points; scores only"},
    "2608.10385": {"C4": "partly: persona prefixes shift LLM relevance assessors (no FP/FN split)", "C5": "context: within families smaller models are more persona-sensitive (context use, not prior use)"},
    "2608.23941": {"C4": "partly: longer review unit makes monitors more rejective, not more discriminative (informedness)"},
    "2608.25869": {"C3": "context: presence of a prior-score anchor matters, its value hardly (parallel to 'presence, not content')", "C2": "context: 'disregard prior scores' warning does not remove the effect", "C4": "partly: context metadata shifts judge scores", "C5": "context: not monotonic in size within Llama"},
    "2608.28725": {"C4": "context: math verifiers falsely reject 76-85% of valid perturbed traces", "C8": "context: test-time compute effects model-dependent"},
    "2608.31016": {"C4": "partly: wording, voting, format and optimisation mostly move the operating point; one affirmative instruction slightly improves discrimination", "C7": "context: AUC-like paired discrimination", "C8": "partly: a reasoning budget raises discrimination (0.546 to 0.669); no prior or payoff"},
    "2609.04270": {"C4": "context: self-review falsely rejects 35% of own correct answers vs 2% cross-family", "C5": "context: reviewer capability tiers"},
    "2609.12439": {"C4": "known paper (not re-screened)"},
    "2609.32616": {"C4": "partly: false accusations (presupposed error) drive agents to damage correct work"},
    "2610.05094": {"C4": "partly: detailed judge prompts cut leniency 81% to 52% with accuracy unchanged", "C8": "partly: reasoning effort (low vs medium) changes neither leniency nor accuracy; no prior or payoff"},
    "2610.06191": {"C6": "context: agents judge results useless yet keep querying", "C3": "context: stated stopping rule/call cost followed only partly", "C8": "context: reasoning mode causes early stops"},
    "2610.11986": {"C4": "context: activation steering moves SDT c of a VLM hazard assessor (not a prompt)"},
    "2610.23988": {"C7": "context: renormalised yes/no token probabilities give AUROC and adjustable thresholds (MLLM clinical classifiers)"},
    "2610.29609": {"C4": "partly: the agent's own success claim shifts completion judges (withholding it raises recall 13-43 pp)"},
    "2610.31414": {"C4": "context: LLM reviewers are harsh on published papers and miss planted flaws (both error types, no manipulation)"},
    "2610.34151": {"C4": "partly: one misleading log line flips correct VLM-judge verdicts", "C2": "context (counterpoint): a one-line warning removes most of the effect"},
    "2610.34488": {"C6": "context: models name a gap and then ignore it (example only)"},
    "2610.35326": {"C1": "context: a stated prior diagnosis shifts SDT c by -0.49 to -1.04 in clinical decisions; categorical prior, no ideal observer", "C4": "context: d' unchanged in 2 of 5 models"},
    "2610.36453": {"C4": "partly: an evidence-gating instruction raises c without raising d' (concession judgments)", "C6": "context: an agent reports changes it did not make", "C5": "context: no simple size trend (Ministral 3B/8B/14B)"},
    "2610.38096": {"C6": "context: models reject infeasible designs when asked only about feasibility but accept them in full answers", "C4": "context: decline wording helps on original items only"},
    "2610.41391": {"C1": "context: LLM reviewers' accept threshold far above the acceptance base rate; base rate never stated, recalibrated post hoc"},
}


def main(ls, out):
    rows = [r for r in csv.DictReader(open(os.path.join(ls, "streams", "arxiv_screening.csv"), newline="", encoding="utf-8"))
            if r["relevance"] == "related"]
    lines = []
    for r in sorted(rows, key=lambda x: x["id"]):
        cov = COV.get(r["id"], {})
        missing = [c for c in r["claims_touched"].split() if c not in cov]
        cov_txt = "; ".join(f"{k} {v}" for k, v in sorted(cov.items())) or "(none)"
        if missing:
            cov_txt += f" [claims field also lists {' '.join(missing)}]"
        lines.append(
            f"- **{r['id']}** {r['title']} ({r['year']}). https://arxiv.org/abs/{r['id']}\n"
            f"  - Manipulation: {r['manipulation'] or 'none'}. Measurement: {r['measurement'] or 'n/a'}.\n"
            f"  - Domain/models: {r['domain_models'] or 'n/a'}. Read: {r['full_text_read'] if r['full_text_read'] != 'no' else 'abstract only'}.\n"
            f"  - Claims: {cov_txt}; all other claims not touched.\n")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(len(rows), "related entries;", sum(1 for r in rows if r["id"] not in COV), "without coverage codes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
