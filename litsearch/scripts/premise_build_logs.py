#!/usr/bin/env python3
"""Build the `premise` stream logs of the claim-test addendum and append them to the merged logs.

Usage:
  python3 -I premise_build_logs.py build     # writes streams/premise_query_log.csv and streams/premise_screening.csv
  python3 -I premise_build_logs.py append    # appends those rows to query_log.csv and screening_log.csv (once)

Counts come from the saved raw data in raw/premise/ and from the lists of titles that were displayed and
read during screening (the *_read / to_read files written while screening). Nothing is fetched here.
`append` adds rows at the end of the merged logs and never rewrites existing rows; query rows carry
`stream=premise` in notes and screening rows a `premise:` prefix in found_via. Relevance in those rows is with
respect to P1-P5. Papers already in screening_log.csv therefore appear twice (once per screening).
"""
import csv
import gzip
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "raw", "premise")
STREAMS = os.path.join(ROOT, "streams")
sys.path.insert(0, HERE)
from premise_rows import ROWS  # noqa: E402

DATE = "2026-11-10"
QCOLS = ["date", "database", "query", "filters", "n_results", "n_screened", "n_kept", "notes"]
SCOLS = ["id", "title", "authors", "year", "venue_or_status", "source_database", "found_via", "relevance",
         "claims_touched", "manipulation", "measurement", "domain_models", "full_text_read", "notes"]
NS = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
csv.field_size_limit(sys.maxsize)


def jl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def lines(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()] if os.path.exists(path) else []


# ---------------------------------------------------------------- metadata
def metadata():
    meta = {}
    for r in jl(os.path.join(RAW, "arxiv", "all_candidates.jsonl")):
        meta.setdefault(r["id"], dict(title=r["title"], authors="; ".join(r["authors"]), year=r["published"][:4],
                                      venue=("arXiv preprint" + (f" ({r['comment'][:90]})" if r.get("comment") else ""))))
    for fn in sorted(os.listdir(os.path.join(RAW, "arxiv"))):
        if fn.startswith("idlist_") and fn.endswith(".xml"):
            for e in ET.parse(os.path.join(RAW, "arxiv", fn)).getroot().findall("a:entry", NS):
                aid = re.sub(r"v\d+$", "", e.findtext("a:id", default="", namespaces=NS).rsplit("/abs/", 1)[-1])
                com = " ".join((e.findtext("ax:comment", default="", namespaces=NS) or "").split())
                meta.setdefault(aid, dict(
                    title=" ".join(e.findtext("a:title", default="", namespaces=NS).split()),
                    authors="; ".join(a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)),
                    year=e.findtext("a:published", default="", namespaces=NS)[:4],
                    venue="arXiv preprint" + (f" ({com[:90]})" if com else "")))
    pages = os.path.join(RAW, "pages")
    for fn in sorted(os.listdir(pages)):
        m = re.match(r"abs_(\d{4}\.\d{4,5})\.html$", fn)
        if not m:
            continue
        s = open(os.path.join(pages, fn), "rb").read().decode("utf-8", "replace")
        g = lambda name: [html.unescape(x) for x in re.findall(r'<meta name="%s" content="([^"]*)"' % name, s)]  # noqa: E731
        c = re.search(r'(?s)<td class="tablecell comments[^"]*">(.*?)</td>', s)
        com = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(c.group(1))).split()) if c else ""
        if g("citation_title"):
            au = "; ".join(" ".join(reversed(a.split(", ", 1))) for a in g("citation_author"))
            meta[m.group(1)] = dict(title=g("citation_title")[0], authors=au, year=(g("citation_date") or ["?"])[0][:4],
                                    venue="arXiv preprint" + (f" ({com[:90]})" if com else ""))
    ordir = os.path.join(RAW, "openreview")
    for fn in sorted(os.listdir(ordir)):
        if fn.endswith(".json.gz"):
            for n in json.loads(gzip.open(os.path.join(ordir, fn)).read()).get("notes", []):
                c = n.get("content", {})

                def val(k):
                    v = c.get(k)
                    v = v.get("value") if isinstance(v, dict) else v
                    if isinstance(v, list):
                        v = "; ".join((x.get("fullname", "") if isinstance(x, dict) else str(x)) for x in v)
                    return v or ""
                fid = n.get("forum") or n.get("id")
                meta.setdefault(fid, dict(title=val("title"), authors=val("authors") or "Anonymous", year="2026",
                                          venue=val("venue")))
    return meta


# ---------------------------------------------------------------- screening rows
def screening(meta):
    out = []
    for pid, r in ROWS.items():
        m = meta.get(pid, {})
        title = r.get("title") or m.get("title")
        if not title:
            raise SystemExit(f"no metadata for {pid}")
        out.append({
            "id": pid, "title": title, "authors": r.get("authors") or m.get("authors", ""),
            "year": r.get("year") or m.get("year", ""), "venue_or_status": r.get("venue") or m.get("venue", ""),
            "source_database": r.get("db", "arXiv API; arxiv.org abstract page"),
            "found_via": "premise:" + r["via"], "relevance": r["rel"], "claims_touched": r["claims"],
            "manipulation": r["manip"], "measurement": r["meas"], "domain_models": r["dom"],
            "full_text_read": r["read"], "notes": "[claim-test screening, Nov 10, 2026; relevance is for P1-P5] " + r["notes"]})
    rank = {"close": 0, "related": 1, "background": 2}
    out.sort(key=lambda x: (rank[x["relevance"]], x["id"]))
    return out


# ---------------------------------------------------------------- query rows
def arxiv_rows(kept):
    rows = []
    d = os.path.join(RAW, "arxiv")
    hits = json.load(open(os.path.join(d, "derived_targeted", "query_hits.json")))
    read = set()
    for i, l in enumerate(lines(os.path.join(d, "derived_targeted", "ranked.tsv"))):
        if i and int(l.split("\t")[0]) >= 9:
            read.add(l.split("\t")[3])
    read |= {l.split("\t")[1] for l in lines(os.path.join(d, "derived_targeted", "band_lt9_filtered.tsv"))}
    read |= set(lines(os.path.join(d, "derived_targeted", "residual_titles_read.txt")))
    qs = {q["qid"]: q for q in jl(os.path.join(d, "queries_premise.jsonl"))}
    for qid in sorted(hits["hits"]):
        ids = set(hits["hits"][qid])
        rows.append([DATE, "arXiv API", qs[qid]["query"], "abstract (and title for P01) fields; sortBy=submittedDate; all pages",
                     hits["totals"][qid], len(ids & read), len(ids & kept),
                     f"{qid}: {qs[qid]['label']}. API terms are stemmed; hits re-matched literally and ranked "
                     f"(premise_arxiv_screen.py); n_screened = titles read"])
    for p in jl(os.path.join(d, "probes.jsonl")):
        if p.get("qid") == "P05" and p["total"] > 10000:
            rows.append([DATE, "arXiv API", p["query"], "count probe only", p["total"], 0, 0,
                         "P05 first form (phrases such as 'contains an error'): not harvested, the API drops stop words; "
                         "replaced by the AND form of P05"])
            break
    rh = json.load(open(os.path.join(d, "derived_recency", "query_hits.json")))
    rq = jl(os.path.join(d, "queries_premise_recency.jsonl"))[0]["query"]
    rec_ids = set(rh["hits"]["PR1_recency"]) | set(rh["hits"]["PR2_recency_oct1_2"])
    rec_read = {l.split("\t")[2] for l in lines(os.path.join(d, "derived_recency", "to_read.tsv"))} | (rec_ids & read)
    rows.append([DATE, "arXiv API", rq, "cs.CL, cs.AI, cs.LG, cs.SE, cs.HC, cs.CY, cs.CR; title or abstract; v1 dates Oct 1 - Nov 10, 2026",
                 rh["totals"]["PR1_recency"], len(rec_read), len(rec_ids & kept),
                 f"PR1 recency sweep: 10,000 records retrieved (HTTP 500 past start=10000); with PR2 all "
                 f"{len(rec_ids)} unique ids are covered. 684 records literally match an evaluator term and a "
                 f"premise term; n_screened = titles read (191 new, the rest via the targeted lists)"])
    rows.append([DATE, "arXiv API", rq.replace("202611102359", "202610022359"),
                 "same query restricted to Oct 1-2, 2026", rh["totals"]["PR2_recency_oct1_2"], 0, 0,
                 "PR2: fetched only to complete the first two days of PR1; screening counted under PR1"])
    pool = lines(os.path.join(d, "nov6_pool_rescreen.tsv"))
    pool_ids = {l.split("\t")[1] for l in pool}
    rows.append([DATE, "local re-screen of the Nov 6 arXiv pools",
                 "raw/arxiv/derived/candidates.jsonl + raw/arxiv/derived_recency/candidates.jsonl, literal evaluator term AND premise term (premise_arxiv_screen.py tags E and A), premise term in the title or 3+ times in the abstract",
                 "2023 on; records not returned by the Nov 10 queries", 15415, len(pool), len(pool_ids & kept),
                 "No request sent: 15,415 unique records saved on Nov 6 re-matched for P1-P5; n_screened = titles read"])
    id_ids = set()
    for f in os.listdir(d):
        if f.startswith("idlist_") and f.endswith(".xml"):
            for e in ET.parse(os.path.join(d, f)).getroot().findall("a:entry", NS):
                id_ids.add(re.sub(r"v\d+$", "", e.findtext("a:id", default="", namespaces=NS).rsplit("/abs/", 1)[-1]))
    n_id = len(id_ids)
    rows.append([DATE, "arXiv API", "id_list lookups of papers reached through citations and reference lists",
                 "id_list", n_id, n_id, len(id_ids & kept),
                 "premise_arxiv_ids.py; abstracts read (cut at 900 characters for triage)"])
    for fn in sorted(os.listdir(d)):
        if fn.startswith("titlecheck_"):
            es = ET.parse(os.path.join(d, fn)).getroot().findall("a:entry", NS)
            rows.append([DATE, "arXiv API", 'ti:"' + fn[len("titlecheck_"):-4].replace("_", " ") + '"', "title field",
                         len(es), len(es), 0, "search for an arXiv copy of an OpenReview-only submission; none found"])
    log = lines(os.path.join(RAW, "fetch_log.tsv"))
    abs_ids = {l.split("\t")[3].rsplit("/abs/", 1)[-1] for l in log if "/abs/" in l and l.split("\t")[1] == "200"}
    n_abs = len(abs_ids)
    n_html_ok = len({l.split("\t")[3] for l in log if "arxiv.org/html/" in l and l.split("\t")[1] == "200"})
    n_html_bad = len({l.split("\t")[3] for l in log if "arxiv.org/html/" in l and l.split("\t")[1] != "200"})
    rows.append([DATE, "arxiv.org abstract pages", "abstract page of every arXiv paper cited in the addendum", "", n_abs, n_abs,
                 len(abs_ids & kept), "premise_fetch.py abs; title, authors, date, comments and abstract checked against what is reported"])
    rows.append([DATE, "arxiv.org HTML full text", "2611.05662, 2603.18740, 2610.32876, 2607.01240, 2606.30587, 2610.06522 (2610.32055 has no HTML version)", "",
                 n_html_ok + n_html_bad, n_html_ok, n_html_ok,
                 "premise_fetch.py html/text/grep/refs; 2611.05662 read in full (main text, App. B, R), the others in the passages named in premise_screening.csv"])
    return rows


REFKW = re.compile(r"sycophan|premise|presuppos|anchor|confirm|bias|fram|defer|trust|authority|hint|false|mislead|persua|judge|review|verif|critic|bayes|base.rate|prior|signal|criterion|credib|source|doubt|pressure|accus|feedback|correct", re.I)


def s2_openalex_rows(kept):
    rows = []
    for l in lines(os.path.join(RAW, "citations_calls.tsv")):
        t, src, kind, aid, st, n = l.split("\t")
        if src == "s2":
            f = os.path.join(RAW, "s2", f"{kind}_{aid}.json")
            key = "citingPaper" if kind == "citations" else "citedPaper"
            ids, n_read = set(), 0
            if os.path.exists(f):
                for row in json.load(open(f)).get("data", []):
                    pp = row.get(key) or {}
                    ext = pp.get("externalIds") or {}
                    pid = ext.get("ArXiv") or ext.get("DOI") or ""
                    ids.add(ext.get("ArXiv") or (ext.get("DOI") or "").lower())
                    shown = f"{pid}|{pp.get('year')}|{(pp.get('title') or '')[:105]}"
                    if kind == "citations" or aid == "2611.05662" or REFKW.search(shown):
                        n_read += 1
            how = ("forward citations; all titles read" if kind == "citations" else
                   "backward citations; all titles read (also from the arXiv HTML bibliography)" if aid == "2611.05662" else
                   "backward citations; n_screened = titles read after a keyword filter (bias, premise, judge, review, trust, ...)")
            rows.append([DATE, "Semantic Scholar Graph API", f"paper/arXiv:{aid}/{kind}", "limit=1000; fields title, externalIds, year, venue, abstract",
                         n, n_read, len(ids & kept), f"HTTP {st}; {how}"])
        elif kind == "citing":
            f = os.path.join(RAW, "openalex", f"citing_{aid}.json")
            ids = {(w.get("doi") or "").lower().replace("https://doi.org/10.48550/arxiv.", "")
                   for w in json.load(open(f)).get("results", [])} if os.path.exists(f) else set()
            rows.append([DATE, "OpenAlex API", f"cites: arXiv:{aid}", "per_page=200", n, n, len(ids & kept),
                         f"HTTP {st}; forward citations; all titles read"])
    d = os.path.join(RAW, "openalex")
    for fn in sorted(os.listdir(d)):
        if not fn.startswith("q_"):
            continue
        j = json.load(open(os.path.join(d, fn)))
        res = j.get("results", [])
        m = re.match(r"q_(.*)_(\d{4}-\d{2}-\d{2})\.json", fn)
        shown = [w for w in res if "arxiv." not in (w.get("doi") or "").lower() or m.group(1).startswith("signal_detection_sycophancy")]
        k = sum(1 for w in res if (w.get("doi") or "").lower().replace("https://doi.org/", "") in
                {x.lower() for x in kept} | {"10.5281/zenodo.23671077", "10.5281/zenodo.23825874"})
        rows.append([DATE, "OpenAlex API", m.group(1).replace("_", " "), f"title_and_abstract.search; from_publication_date {m.group(2)}; per_page=50, first page",
                     j.get("meta", {}).get("count"), len(shown), k,
                     "keyless shared budget, so first page only; n_screened = titles read (records without an arXiv DOI; arXiv records are covered by the arXiv queries)"])
    return rows


def openreview_rows(kept):
    d = os.path.join(RAW, "openreview")
    via = {}
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".json.gz"):
            ph = fn.split("__")[0]
            for n in json.loads(gzip.open(os.path.join(d, fn)).read()).get("notes", []):
                via.setdefault(n.get("forum") or n.get("id"), set()).add(ph)
    kw = re.compile(r"sycophan|premise|presuppos|anchor|confirm|defer|trust|authority|hint|false|mislead|persua|judge|review|verif|critic|bayes|base.rate|prior|signal|criterion|credib|source|doubt|pressure|accus|feedback|told|assert|suggest|bias|grader|audit|monitor|error|mistake|proof", re.I)
    read = set()
    for l in lines(os.path.join(d, "to_read.tsv")):
        f = l.split("\t")
        shown = f"{f[0]} {f[2]} {f[3]}|{f[4][:22]}|{f[5][:105]}"
        if "|CoRR 20" not in shown and kw.search(shown):
            read.add(f[3])
    rows = []
    for l in lines(os.path.join(d, "queries.tsv")):
        t, ph, total, got = l.split("\t")
        slug = re.sub(r"[^a-z0-9]+", "_", ph.lower()).strip("_")
        ids = {k for k, v in via.items() if slug in v}
        rows.append([DATE, "OpenReview API v2 /notes/search", f'"{ph}"', "content=all; source=forum; all groups; up to 3 pages of 1000",
                     total, len(ids & read), len(ids & kept),
                     f"fetched {got}; matched locally for 2023 on, an LLM term and the P1-P5 tags (premise_openreview.py rank); n_screened = titles read"])
    return rows


def crossref_rows():
    d = os.path.join(RAW, "crossref")
    kw = re.compile(r"sycophan|presuppos|premise|confirmation|anchor|defer|authority|mislead|pushback|pressure|gullib|persua|conform|epistemic|hint|base.rate|bayes|signal detection|self-correct|doubt|stubborn|judge", re.I)
    shown = [l for l in lines(os.path.join(d, "to_read.txt"))[1:] if kw.search(l)][:150]
    read = {l.split("|")[0].split(" ", 1)[1].lower() for l in shown}
    names = {"acl": "ACL Anthology, prefix 10.18653", "acm": "ACM, prefix 10.1145", "aaai": "AAAI, prefix 10.1609", "ieee": "IEEE, prefix 10.1109"}
    rows = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".json"):
            j = json.load(open(os.path.join(d, fn)))["message"]
            q, p = fn[:-5].split("__")
            ids = {it.get("DOI", "").lower() for it in j.get("items", [])}
            rows.append([DATE, f"Crossref API ({names[p]})", q.replace("_", " "), "query.bibliographic; from-pub-date 2023-01-01; top 100 by relevance",
                         j.get("total-results"), len(ids & read), 0,
                         "relevance-ranked OR match, so totals are not meaningful; n_screened = titles read after a local term filter"])
    return rows


def other_rows():
    return [
        [DATE, "ACL Anthology pages", "2026.gem-main.45; 2026.findings-acl.2087; 2026.findings-emnlp.1571; 2026.emnlp-main.157", "", 4, 4, 0,
         "abstracts read for four Crossref hits; none bears on P1-P5 beyond background"],
        [DATE, "Zenodo API", "records 23671078 (Quiroz) and 23825874 (Porcaro)", "", 2, 2, 2, "record descriptions read"],
        [DATE, "Web search (WebSearch tool, standard mode)", 'LLM verifier told "contains an error" false positives correct solutions presupposition study 2026', "", 10, 10, 0,
         "no study with an asserted-error prompt on correct solutions; pointed to papers already screened"],
        [DATE, "Web search (WebSearch tool, standard mode)", 'signal detection theory sycophancy LLM criterion shift not sensitivity assertion "false alarm" judge 2026', "", 10, 10, 0,
         "returned Cacioli 2603.14893 (known) and a sycophancy position paper; nothing new"],
        [DATE, "Web search (WebSearch tool, standard mode)", 'LLM code review "there is a bug" prompt hallucinated bugs presupposed bug experiment false positive rate assertion vs "check carefully"', "", 10, 10, 0,
         "returned 2603.18740 and 2603.00539 (both known); no scrutiny-vs-assertion control found"],
    ]


def build():
    meta = metadata()
    srows = screening(meta)
    kept = {r["id"] for r in srows}
    with open(os.path.join(STREAMS, "premise_screening.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, SCOLS)
        w.writeheader()
        w.writerows(srows)
    qrows = arxiv_rows(kept) + s2_openalex_rows(kept) + openreview_rows(kept) + crossref_rows() + other_rows()
    with open(os.path.join(STREAMS, "premise_query_log.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(QCOLS)
        w.writerows(qrows)
    from collections import Counter
    print(f"screening rows: {len(srows)} {dict(Counter(r['relevance'] for r in srows))}")
    print(f"query rows: {len(qrows)} {dict(Counter(q[1].split(' (')[0] for q in qrows))}")

    def num(x):
        try:
            return int(x)
        except (TypeError, ValueError):
            return 0
    print(f"sum n_results: {sum(num(q[4]) for q in qrows)}  sum n_screened: {sum(num(q[5]) for q in qrows)}")


def append():
    q = list(csv.reader(open(os.path.join(STREAMS, "premise_query_log.csv"), encoding="utf-8")))[1:]
    s = list(csv.DictReader(open(os.path.join(STREAMS, "premise_screening.csv"), encoding="utf-8")))
    qpath, spath = os.path.join(ROOT, "query_log.csv"), os.path.join(ROOT, "screening_log.csv")
    if any("stream=premise" in l for l in open(qpath, encoding="utf-8")):
        raise SystemExit("premise rows are already in query_log.csv; nothing appended")
    old_ids = {r["id"] for r in csv.DictReader(open(spath, encoding="utf-8"))}
    with open(qpath, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        for r in q:
            w.writerow(r[:7] + ["stream=premise; " + r[7]])
    with open(spath, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, SCOLS)
        w.writerows(s)
    dup = sum(1 for r in s if r["id"] in old_ids)
    print(f"appended {len(q)} query rows and {len(s)} screening rows ({dup} re-screen papers already in the log, {len(s) - dup} new ids)")


if __name__ == "__main__":
    {"build": build, "append": append}[sys.argv[1]]()
