"""Resolve known arXiv papers via free OpenAlex singleton lookups (doi:10.48550/arXiv.<id>).
Writes $PEER_SCRATCH/known_resolved.jsonl with title, year, and all locations (venues)."""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402
rows = list(csv.DictReader(open(os.path.join(L.LS, "known_papers.csv"))))
out = open(os.path.join(L.SCRATCH, "known_resolved.jsonl"), "w")
for r in rows:
    aid = r["id"]
    url = f"https://api.openalex.org/works/doi:10.48550/arXiv.{aid}"
    try:
        d = L.get_json(url, {"select": "id,doi,title,publication_year,locations,authorships,ids"},
                       source="openalex_known", raw_name="known_" + aid, max_retries=1)
        locs = [f"{(l.get('source') or {}).get('display_name')} [{(l.get('source') or {}).get('type')}] {l.get('landing_page_url')}"
                for l in d.get("locations") or []]
        rec = {"arxiv": aid, "short": r["short_title"], "title": d.get("title"), "year": d.get("publication_year"),
               "openalex": d.get("id"), "locations": locs,
               "authors": "; ".join((a.get("author") or {}).get("display_name", "") for a in d.get("authorships") or [])}
    except Exception as e:
        rec = {"arxiv": aid, "short": r["short_title"], "error": str(e)[:200]}
    out.write(json.dumps(rec) + "\n"); out.flush()
    print(aid, "|", rec.get("title") or rec.get("error"), "|", [x for x in rec.get("locations", []) if "arXiv" not in x])
