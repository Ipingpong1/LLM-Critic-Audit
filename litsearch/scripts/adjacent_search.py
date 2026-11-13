#!/usr/bin/env python3
"""Search helper for the `adjacent` stream.

Sources: Semantic Scholar (s2), OpenAlex (oa), Crossref (cr / crq), arXiv API (ax).
Raw responses go to ../raw/adjacent/. Every search is appended to a staging
query log (TSV) in the scratchpad given by ADJ_STAGE (default: ./_adj_stage.tsv).

Rate limits (streams/README.md): S2 >= 2 s between calls, 60 s wait on 429
(max 5 retries); OpenAlex / Crossref <= 2 req/s; arXiv >= 10 s between calls
for this stream. No API keys, no mailto.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "adjacent")
os.makedirs(RAW, exist_ok=True)
STAGE = os.environ.get("ADJ_STAGE", os.path.join(os.getcwd(), "_adj_stage.tsv"))
import tempfile
STAMP = os.path.join(tempfile.gettempdir(), "adjacent_last_call_times.json")  # rate-limit stamps, kept out of raw/
UA = "critic-sdt-litsearch/0.1 (academic literature search; no contact)"

MIN_GAP = {"s2": 2.2, "oa": 0.6, "cr": 0.6, "ax": 10.5}


def _wait(src):
    try:
        with open(STAMP) as f:
            t = json.load(f)
    except Exception:
        t = {}
    last = t.get(src, 0)
    gap = MIN_GAP[src] - (time.time() - last)
    if gap > 0:
        time.sleep(gap)
    t[src] = time.time()
    with open(STAMP, "w") as f:
        json.dump(t, f)


def _get(src, url, accept="application/json"):
    retries = 0
    while True:
        _wait(src)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and retries < 5:
                retries += 1
                sys.stderr.write(f"[{src}] 429, waiting 60 s (retry {retries}/5)\n")
                time.sleep(60)
                continue
            if e.code == 404:
                return None
            raise


def _slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s)[:60].strip("_")


def _save(src, q, text, ext="json"):
    fn = os.path.join(RAW, f"{src}_{datetime.now().strftime('%Y%m%dT%H%M%S')}_{_slug(q)}.{ext}")
    with open(fn, "w") as f:
        f.write(text)
    return fn


def _stage(database, query, filters, n_results, n_shown):
    new = not os.path.exists(STAGE)
    with open(STAGE, "a") as f:
        if new:
            f.write("date\tdatabase\tquery\tfilters\tn_results\tn_shown\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d')}\t{database}\t{query}\t{filters}\t{n_results}\t{n_shown}\n")


def _abbrev(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def s2(query, limit=20, year="2022-2026", show_abs=200):
    params = {
        "query": query,
        "limit": str(limit),
        "fields": "title,year,venue,externalIds,abstract,authors,citationCount,publicationDate",
    }
    if year:
        params["year"] = year
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(params)
    text = _get("s2", url)
    _save("s2", query, text or "{}")
    d = json.loads(text or "{}")
    total = d.get("total", 0)
    data = d.get("data", []) or []
    _stage("Semantic Scholar API", query, f"year={year}; limit={limit}", total, len(data))
    print(f"# S2 total={total} shown={len(data)} :: {query}")
    for i, p in enumerate(data, 1):
        ext = p.get("externalIds") or {}
        ids = []
        if ext.get("ArXiv"):
            ids.append("arXiv:" + ext["ArXiv"])
        if ext.get("DOI"):
            ids.append("doi:" + ext["DOI"])
        au = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:3])
        if len(p.get("authors") or []) > 3:
            au += " et al."
        print(f"{i:2d}. [{p.get('year')}] {_abbrev(p.get('title'), 150)} | {au} | {_abbrev(p.get('venue'), 40)} | {' '.join(ids)} | cit={p.get('citationCount')}")
        if show_abs:
            print("    " + _abbrev(p.get("abstract"), show_abs))


def _oa_abstract(inv):
    if not inv:
        return ""
    pos = []
    for w, idxs in inv.items():
        for i in idxs:
            pos.append((i, w))
    return " ".join(w for _, w in sorted(pos))


def oa(query, per_page=25, from_date="2022-01-01", mode="ta", show_abs=200, extra_filter=""):
    """mode 'ta' = title_and_abstract.search filter; 'all' = search= (incl. fulltext)."""
    params = {"per-page": str(per_page)}
    filters = []
    if from_date:
        filters.append(f"from_publication_date:{from_date}")
    if extra_filter:
        filters.append(extra_filter)
    if mode == "ta":
        filters.append(f"title_and_abstract.search:{query}")
        params["sort"] = "relevance_score:desc"
    elif mode == "title":
        filters.append(f"title.search:{query}")
        params["sort"] = "relevance_score:desc"
    else:
        params["search"] = query
    if filters:
        params["filter"] = ",".join(filters)
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    text = _get("oa", url)
    _save("oa", query, text or "{}")
    d = json.loads(text or "{}")
    total = (d.get("meta") or {}).get("count", 0)
    res = d.get("results", []) or []
    _stage("OpenAlex API", query, f"mode={mode}; from={from_date}; {extra_filter}; per_page={per_page}", total, len(res))
    print(f"# OA total={total} shown={len(res)} :: {query}")
    for i, w in enumerate(res, 1):
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        au = ", ".join(((a.get("author") or {}).get("display_name") or "") for a in (w.get("authorships") or [])[:3])
        if len(w.get("authorships") or []) > 3:
            au += " et al."
        print(f"{i:2d}. [{w.get('publication_year')}] {_abbrev(w.get('title'), 150)} | {au} | {_abbrev(src, 45)} | doi:{doi} | cit={w.get('cited_by_count')}")
        if show_abs:
            print("    " + _abbrev(_oa_abstract(w.get("abstract_inverted_index")), show_abs))


def cr(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    text = _get("cr", url)
    if text is None:
        print(f"# CR {doi}: NOT FOUND (404)")
        return
    _save("cr", doi, text)
    m = json.loads(text)["message"]
    au = "; ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in m.get("author", []))
    yr = None
    for k in ("published-print", "published-online", "issued", "created"):
        if m.get(k, {}).get("date-parts"):
            yr = m[k]["date-parts"][0][0]
            break
    print(f"# CR {doi}\n  title: {(m.get('title') or [''])[0]}\n  authors: {au}\n  year: {yr}\n  journal: {(m.get('container-title') or [''])[0]} vol {m.get('volume')} issue {m.get('issue')} pages {m.get('page')}\n  type: {m.get('type')}  publisher: {m.get('publisher')}")
    if m.get("abstract"):
        print("  abstract: " + _abbrev(re.sub('<[^>]+>', ' ', m['abstract']), 1500))


def crq(q, rows=5):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": str(rows)})
    text = _get("cr", url)
    _save("crq", q, text or "{}")
    items = json.loads(text)["message"]["items"]
    print(f"# CRQ :: {q}")
    for i, m in enumerate(items, 1):
        au = "; ".join(a.get("family", "") for a in m.get("author", [])[:4])
        yr = None
        for k in ("published-print", "published-online", "issued"):
            if m.get(k, {}).get("date-parts"):
                yr = m[k]["date-parts"][0][0]
                break
        print(f"{i}. [{yr}] {(m.get('title') or [''])[0]} | {au} | {(m.get('container-title') or [''])[0]} {m.get('volume')}({m.get('issue')}):{m.get('page')} | doi:{m.get('DOI')}")


def ax(query, max_results=25):
    params = {"search_query": query, "start": "0", "max_results": str(max_results), "sortBy": "relevance"}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    text = _get("ax", url, accept="application/atom+xml")
    _save("ax", query, text or "", ext="xml")
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    root = ET.fromstring(text)
    total = root.findtext("o:totalResults", default="?", namespaces=ns)
    ents = root.findall("a:entry", ns)
    _stage("arXiv API", query, f"max_results={max_results}; sort=relevance", total, len(ents))
    print(f"# arXiv total={total} shown={len(ents)} :: {query}")
    for i, e in enumerate(ents, 1):
        aid = e.findtext("a:id", default="", namespaces=ns).rsplit("/", 1)[-1]
        t = _abbrev(e.findtext("a:title", default="", namespaces=ns), 150)
        pub = e.findtext("a:published", default="", namespaces=ns)[:10]
        au = ", ".join(a.findtext("a:name", default="", namespaces=ns) for a in e.findall("a:author", ns)[:3])
        print(f"{i:2d}. [{pub}] {t} | {au} | arXiv:{aid}")
        print("    " + _abbrev(e.findtext("a:summary", default="", namespaces=ns), 200))


def s2paper(pid, fields="title,year,venue,externalIds,abstract,authors,publicationVenue,journal,tldr"):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(pid, safe=':')}?fields={fields}"
    text = _get("s2", url)
    if text is None:
        print(f"# S2 paper {pid}: not found")
        return
    _save("s2paper", pid, text)
    p = json.loads(text)
    au = ", ".join(a.get("name", "") for a in p.get("authors") or [])
    print(f"# {pid}\n  {p.get('title')} ({p.get('year')}) | {p.get('venue')} | {p.get('journal')}\n  authors: {au}\n  ids: {p.get('externalIds')}\n  abstract: {p.get('abstract')}")


def axid(ids, show_abs=900):
    """Fetch abstracts for a comma-separated list of arXiv ids (one API call)."""
    params = {"id_list": ids, "max_results": str(len(ids.split(",")))}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    text = _get("ax", url, accept="application/atom+xml")
    _save("axid", ids[:50], text or "", ext="xml")
    ns = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(text)
    for e in root.findall("a:entry", ns):
        aid = e.findtext("a:id", default="", namespaces=ns).rsplit("/", 1)[-1]
        t = re.sub(r"\s+", " ", e.findtext("a:title", default="", namespaces=ns))
        pub = e.findtext("a:published", default="", namespaces=ns)[:10]
        upd = e.findtext("a:updated", default="", namespaces=ns)[:10]
        au = "; ".join(a.findtext("a:name", default="", namespaces=ns) for a in e.findall("a:author", ns))
        jr = e.findtext("ax:journal_ref", default="", namespaces=ns)
        cm = e.findtext("ax:comment", default="", namespaces=ns)
        print(f"== {aid} [{pub}; upd {upd}] {t}\n   AU: {au}\n   JR: {jr} | CM: {cm}\n   AB: {_abbrev(e.findtext('a:summary', default='', namespaces=ns), show_abs)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = sys.argv[2:]
    kw = {}
    pos = []
    for a in args:
        if a.startswith("--") and "=" in a:
            k, v = a[2:].split("=", 1)
            kw[k] = int(v) if v.isdigit() else v
        else:
            pos.append(a)
    {"s2": s2, "oa": oa, "cr": cr, "crq": crq, "ax": ax, "axid": axid, "s2paper": s2paper}[cmd](*pos, **kw)
