#!/usr/bin/env python3
"""Write streams/arxiv_query_log.csv and streams/arxiv_screening.csv for the `arxiv` stream.

Usage: python3 -I arxiv_write_outputs.py <litsearch_dir>

Inputs (under <litsearch_dir>/raw/arxiv/): manifest.jsonl (harvested pages), probes.jsonl (count probes),
idlist_calls.jsonl (id_list fetches), derived*/ranked.jsonl (candidates with literal block matches and
tiers, from arxiv_rank.py), derived/tfilter_*.tsv (literal re-match of targeted queries),
derived_recency/recency_list.tsv (literal recency-term matches), derived/screened_title_ids.txt (every
id whose title was read), derived/decisions.jsonl (abstract/full-text decisions; later lines override
earlier ones), derived/query_notes.json (optional per-query notes).
"""
import csv
import glob
import json
import os
import sys

DB = "arXiv API (export.arxiv.org/api/query)"


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


def main(ls):
    rd = os.path.join(ls, "raw", "arxiv")
    manifest = jl(os.path.join(rd, "manifest.jsonl"))
    probes = jl(os.path.join(rd, "probes.jsonl"))
    idcalls = jl(os.path.join(rd, "idlist_calls.jsonl"))
    cands = {}
    for p in sorted(glob.glob(os.path.join(rd, "derived*", "ranked.jsonl"))):
        for r in jl(p):
            c = cands.setdefault(r["id"], r)
            for q in r["found_via"]:
                if q not in c["found_via"]:
                    c["found_via"].append(q)
    screened = {l.strip() for l in open(os.path.join(rd, "derived", "screened_title_ids.txt"), encoding="utf-8") if l.strip()}
    dec = {}
    for d in jl(os.path.join(rd, "derived", "decisions.jsonl")):
        dec.setdefault(d["id"], {}).update({k: v for k, v in d.items() if v not in (None, "")})
    qnotes = {}
    p = os.path.join(rd, "derived", "query_notes.json")
    if os.path.exists(p):
        qnotes = json.load(open(p, encoding="utf-8"))
    literal = {}  # qid -> set of ids literally matching that query's own term groups
    for f in glob.glob(os.path.join(rd, "derived", "tfilter_*.tsv")):
        for line in open(f, encoding="utf-8"):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                literal.setdefault(parts[0], set()).add(parts[1])
    rec_lit = set()
    p = os.path.join(rd, "derived_recency", "recency_list.tsv")
    if os.path.exists(p):
        for i, line in enumerate(open(p, encoding="utf-8")):
            if i:
                rec_lit.add(line.split("\t")[1])
    kept_rel = {"background", "related", "close"}
    ids_by_q = {}
    for aid, r in cands.items():
        for q in r["found_via"]:
            ids_by_q.setdefault(q, set()).add(aid)

    rows = []
    harvested = {m["qid"] for m in manifest}
    for pr in probes:
        if pr.get("tag") == "plan-probe" and pr.get("qid") in harvested:
            continue
        qid = pr.get("qid") or ""
        if pr.get("tag") == "stemming-probe":
            filt, note = "no date filter; count probe (max_results=1)", "Count probe to test API stemming/tokenisation; not screened"
        else:
            filt = "date filter inside query; count probe (max_results=1)"
            note = qnotes.get(qid) or ("Count probe; 0 hits, nothing to harvest" if pr["total"] == 0 else "Count probe only; not harvested")
            note = f"[{qid}] " + note
        rows.append([pr["fetched_utc"][:10], DB, pr["query"], filt, pr["total"], 0, 0, note])
    seen = set()
    for m in manifest:
        q = m["qid"]
        if q in seen:
            continue
        seen.add(q)
        ids = ids_by_q.get(q, set())
        n_scr = sum(1 for i in ids if i in screened)
        n_keep = sum(1 for i in ids if dec.get(i, {}).get("relevance") in kept_rel)
        n_known = sum(1 for i in ids if cands.get(i, {}).get("known"))
        tiers = {t: sum(1 for i in ids if cands.get(i, {}).get("tier") == t) for t in (1, 2, 3, 4, 5)}
        if q.startswith("T") or q.startswith("X0") or q.startswith("X1") and not q.startswith("X15"):
            lit = literal.get(q, set())
            cut = (f"literal re-match of this query's own term groups: {len(lit)} of {len(ids)} (all titles read); "
                   f"the rest are API stemming matches (e.g. utility=utilize, critic=critical)")
        elif q.startswith("R1"):
            cut = (f"literal recency-term match {len(rec_lit)} of {len(ids)} (all titles read; "
                   f"{len(ids) - len(rec_lit)} stemming-only matches such as critical/review/monitoring not read)")
        elif q.startswith("X15b"):
            cut = "corrected X15 (ANDNOT at the end); literal block-A + strong B/C matches read"
        elif q.startswith("X15"):
            cut = ("MALFORMED: ANDNOT grouped the category and date filters into the negation, so results include "
                   "pre-2022 and non-CS records; literal block-A + strong B/C matches (488) all read; superseded by X15b")
        else:
            cut = (f"literal block match tiers 1-3 (A and B/C) {tiers[1] + tiers[2] + tiers[3]}, tier 4 (strong B/C, no "
                   f"literal A) {tiers[4]}: all titles read; tier 5 {tiers[5]} (stemming over-reach or A without literal "
                   f"B/C) not title-screened")
        extra = qnotes.get(q, "")
        note = f"[{q}] retrieved {len(ids)} unique ids; " + cut
        if n_known:
            note += f"; {n_known} already in known_papers.csv"
        if extra:
            note += "; " + extra
        filt = "sortBy=submittedDate desc; abs:/ti:/cat: fields as written (API stems terms); max_results=1000 per page"
        rows.append([m["fetched_utc"][:10], DB, m["query"], filt, m["total"], n_scr, n_keep, note])
    for c in idcalls:
        rows.append([c["fetched_utc"][:10], DB, "id_list=" + ",".join(c["ids"]), "id_list fetch (recall check of known papers missing from the block queries)",
                     c["total"], c["n_entries"], 0, "Known-paper recall check: 4 lack any block B/C term, 2 lack 'LLM'/'language model' (see notes)"])
    out = os.path.join(ls, "streams", "arxiv_query_log.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["date", "database", "query", "filters", "n_results", "n_screened", "n_kept", "notes"])
        w.writerows(rows)
    print("query log rows:", len(rows), "->", out)

    out2 = os.path.join(ls, "streams", "arxiv_screening.csv")
    order = {"close": 0, "related": 1, "background": 2}
    keep = sorted(((i, d) for i, d in dec.items() if d.get("relevance") in kept_rel),
                  key=lambda x: (order[x[1]["relevance"]], x[0]))
    with open(out2, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["id", "title", "authors", "year", "venue_or_status", "source_database", "found_via", "relevance",
                    "claims_touched", "manipulation", "measurement", "domain_models", "full_text_read", "notes"])
        for aid, d in keep:
            c = cands.get(aid, {})
            au = c.get("authors", [])
            authors = "; ".join(au[:6]) + ("; et al." if len(au) > 6 else "")
            venue = c.get("journal_ref") or ""
            if not venue:
                venue = "arXiv preprint" + (f" ({c['comment'][:160]})" if c.get("comment") else "")
            fv = "; ".join(sorted(c.get("found_via", []))) or "id_list recall check"
            ver = (",".join(c.get("versions", [])) or "")
            notes = d.get("notes", "")
            if ver:
                notes = (notes + f" [arXiv versions seen: {ver}]").strip()
            w.writerow([aid, c.get("title", d.get("title", "")), authors, c.get("published", "")[:4], venue, "arXiv API",
                        fv, d["relevance"], d.get("claims", ""), d.get("manipulation", ""), d.get("measurement", ""),
                        d.get("domain_models", ""), d.get("full_text_read", "no"), notes])
    print("screening rows:", len(keep), "->", out2)


if __name__ == "__main__":
    main(sys.argv[1])
