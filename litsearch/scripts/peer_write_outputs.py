"""Write streams/peer_query_log.csv and streams/peer_screening.csv.

Inputs (scratchpad):
  peer_qlog.jsonl        one row per query actually run (written by the runners)
  screen_records.json    list of screening decisions (background or above), each with
                         'corpus_keys': [(src, key), ...] linking it to retrieved records
  seen_<src>.txt         keys of records whose titles were screened
  <src>_dedup.jsonl      deduplicated corpora with found_via (query||filter) lists
n_screened per query = retrieved records of that query whose title was screened;
n_kept per query = retrieved records of that query that map to a screening row.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

OUT_Q = os.path.join(L.LS, "streams", "peer_query_log.csv")
OUT_S = os.path.join(L.LS, "streams", "peer_screening.csv")
QCOLS = ["date", "database", "query", "filters", "n_results", "n_screened", "n_kept", "notes"]
SCOLS = ["id", "title", "authors", "year", "venue_or_status", "source_database", "found_via", "relevance",
         "claims_touched", "manipulation", "measurement", "domain_models", "full_text_read", "notes"]


def load_seen(src):
    p = os.path.join(L.SCRATCH, f"seen_{src}.txt")
    return set(x.strip() for x in open(p)) if os.path.exists(p) else set()


def main():
    recs = json.load(open(os.path.join(L.SCRATCH, "screen_records.json")))
    kept = {"or": set(), "cr": set(), "oa": set()}
    for r in recs:
        for src, key in r.get("corpus_keys", []):
            kept[src].add(key)
    # per-query screened/kept counts
    qstat = {}
    for src in ("or", "cr", "oa"):
        p = os.path.join(L.SCRATCH, f"{src}_dedup.jsonl")
        if not os.path.exists(p):
            continue
        seen = load_seen(src)
        for line in open(p):
            r = json.loads(line)
            for fv in r["found_via"]:
                st = qstat.setdefault((src, fv), [0, 0])
                if r["key"] in seen:
                    st[0] += 1
                if r["key"] in kept[src]:
                    st[1] += 1
    rows = [json.loads(l) for l in open(L.QLOG)]
    with open(OUT_Q, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=QCOLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            db = r["database"]
            if db.startswith("OpenReview"):
                grp = r["filters"].split(";")[0].replace("group=", "").strip()
                key = ("or", f"{r['query']}||{grp}")
            elif db.startswith("Crossref"):
                flt = r["filters"].split("filter=")[1].split(";")[0].strip() if "filter=" in r["filters"] else ""
                key = ("cr", f"{r['query']}||{flt}")
            elif db.startswith("OpenAlex"):
                key = ("oa", r["query"])
            else:
                key = None
            st = qstat.get(key, None) if key else None
            if r.get("n_screened") in ("", None):
                r["n_screened"] = st[0] if st else (0 if key else "")
            if r.get("n_kept") in ("", None):
                r["n_kept"] = st[1] if st else (0 if key else "")
            w.writerow({k: r.get(k, "") for k in QCOLS})
    with open(OUT_S, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCOLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in recs:
            w.writerow({k: r.get(k, "") for k in SCOLS})
    print(f"wrote {len(rows)} query rows -> {OUT_Q}")
    print(f"wrote {len(recs)} screening rows -> {OUT_S}")


if __name__ == "__main__":
    main()
