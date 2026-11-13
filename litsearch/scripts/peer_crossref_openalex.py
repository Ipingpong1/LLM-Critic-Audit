"""Crossref and OpenAlex runners for the `peer` stream.

Usage:
  python3 -I peer_crossref_openalex.py crossref TASKS.json
  python3 -I peer_crossref_openalex.py openalex TASKS.json

Crossref task: {"q": query.bibliographic string, "filter": "prefix:10.18653,from-pub-date:2022-01-01",
                "rows": 100, "tag": "..."}
OpenAlex task: {"q": boolean string for title_and_abstract.search, "filter_extra": "", "max_pages": 5,
                "tag": "..."}
No mailto / email / API key is sent.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

CR_CORPUS = os.path.join(L.SCRATCH, "cr_corpus.jsonl")
OA_CORPUS = os.path.join(L.SCRATCH, "oa_corpus.jsonl")


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def loose_hit(text):
    cl = L.classify(text)
    loose = cl["LLM"] and bool(cl["A"] or cl["B"] or cl["C"])
    return cl, loose


def run_crossref(t):
    params = {
        "query.bibliographic": t["q"],
        "filter": t["filter"],
        "rows": t.get("rows", 100),
        "select": "DOI,title,author,container-title,issued,type,abstract,score,URL,publisher",
    }
    name = "cr__" + L.slug(t["filter"], 40) + "__" + L.slug(t["q"], 60)
    d = L.get_json("https://api.crossref.org/works", params, source="crossref", raw_name=name)
    msg = d.get("message", {})
    items = msg.get("items", [])
    total = msg.get("total-results")
    n_loose = n_strict = 0
    with open(CR_CORPUS, "a") as f:
        for it in items:
            title = strip_tags(" ".join(it.get("title") or []))
            abstract = strip_tags(it.get("abstract") or "")
            authors = "; ".join(
                (a.get("given", "") + " " + a.get("family", "")).strip() for a in (it.get("author") or [])
            )
            yr = None
            try:
                yr = it["issued"]["date-parts"][0][0]
            except Exception:
                pass
            cl, loose = loose_hit(title + " " + abstract)
            n_loose += loose
            n_strict += cl["hit"]
            rec = {
                "doi": it.get("DOI"), "title": title, "abstract": abstract, "authors": authors,
                "year": yr, "venue": " ".join(it.get("container-title") or []), "type": it.get("type"),
                "publisher": it.get("publisher"), "url": it.get("URL"), "score": it.get("score"),
                "found_via": f"{t['q']}||{t['filter']}", "cl": cl, "loose": loose,
            }
            f.write(json.dumps(rec) + "\n")
    note = (f"{t.get('tag','')}; relevance-ranked (OR semantics); took top {len(items)}; "
            f"{n_loose} pass loose filter (LLM & any block term), {n_strict} pass A&LLM&(B|C)")
    L.log_query("Crossref works API", t["q"], f"query.bibliographic; filter={t['filter']}; rows={params['rows']}",
                total, notes=note)
    print(f"CR {t['filter'][:30]:30} {t['q'][:55]:55} total={total} top={len(items)} loose={n_loose} strict={n_strict}",
          flush=True)


def inv_to_text(inv):
    if not inv:
        return ""
    pos = []
    for w, ps in inv.items():
        for p in ps:
            pos.append((p, w))
    return " ".join(w for _, w in sorted(pos))


def run_openalex(t):
    flt = "from_publication_date:2022-01-01,title_and_abstract.search:" + t["q"]
    if t.get("filter_extra"):
        flt += "," + t["filter_extra"]
    got, count, page = [], None, 1
    while True:
        params = {
            "filter": flt, "per-page": 200, "page": page,
            "select": "id,doi,title,publication_year,type,primary_location,locations,authorships,"
                      "abstract_inverted_index,ids",
        }
        name = "oa__" + L.slug(t["q"], 80) + f"__p{page}"
        d = L.get_json("https://api.openalex.org/works", params, source="openalex", raw_name=name)
        res = d.get("results", [])
        count = d.get("meta", {}).get("count")
        got.extend(res)
        if not res or page * 200 >= (count or 0) or page >= t.get("max_pages", 5):
            break
        page += 1
    n_strict = 0
    with open(OA_CORPUS, "a") as f:
        for w in got:
            abstract = inv_to_text(w.get("abstract_inverted_index"))
            title = w.get("title") or ""
            locs = []
            for loc in w.get("locations") or []:
                src = (loc or {}).get("source") or {}
                if src.get("display_name"):
                    locs.append(f"{src.get('display_name')} [{src.get('type')}]")
            pl = ((w.get("primary_location") or {}).get("source") or {})
            cl = L.classify(title + " " + abstract)
            n_strict += cl["hit"]
            rec = {
                "openalex": w.get("id"), "doi": w.get("doi"), "ids": w.get("ids"), "title": title,
                "abstract": abstract, "year": w.get("publication_year"), "type": w.get("type"),
                "primary_source": f"{pl.get('display_name')} [{pl.get('type')}]",
                "locations": locs,
                "authors": "; ".join(((a.get("author") or {}).get("display_name") or "")
                                     for a in (w.get("authorships") or [])[:12]),
                "found_via": t["q"], "cl": cl,
            }
            f.write(json.dumps(rec) + "\n")
    note = (f"{t.get('tag','')}; boolean title_and_abstract.search; retrieved {len(got)} of {count}; "
            f"{n_strict} pass local A&LLM&(B|C)")
    L.log_query("OpenAlex works API", t["q"],
                f"filter=from_publication_date:2022-01-01,title_and_abstract.search"
                + (("," + t["filter_extra"]) if t.get("filter_extra") else "") + "; per-page=200",
                count, notes=note)
    print(f"OA {t['q'][:90]:90} count={count} got={len(got)} strict={n_strict}", flush=True)


def main():
    mode, path = sys.argv[1], sys.argv[2]
    tasks = json.load(open(path))
    done_path = os.path.join(L.SCRATCH, f"{mode}_done.txt")
    done = set(x.strip() for x in open(done_path)) if os.path.exists(done_path) else set()
    for t in tasks:
        key = t["q"] + "||" + t.get("filter", t.get("filter_extra", ""))
        if key in done:
            continue
        try:
            (run_crossref if mode == "crossref" else run_openalex)(t)
            with open(done_path, "a") as f:
                f.write(key + "\n")
        except Exception as e:
            print("FAILED", t, str(e)[:300], flush=True)
            L.log_query("Crossref works API" if mode == "crossref" else "OpenAlex works API", t["q"],
                        t.get("filter", t.get("filter_extra", "")), "", notes=f"FAILED: {str(e)[:200]}")


if __name__ == "__main__":
    main()
