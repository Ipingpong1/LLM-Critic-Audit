#!/usr/bin/env python3
"""Write streams/citations_query_log.csv from the raw files + hand-entered screening counts (python3 -I).

n_results is read from the saved raw response; n_screened / n_kept / notes come from SCREEN below.
"""
import csv
import glob
import json
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
LS = os.path.dirname(HERE)
RAW = os.path.join(LS, "raw", "citations")
OUT = os.path.join(LS, "streams", "citations_query_log.csv")
COLS = ["date", "database", "query", "filters", "n_results", "n_screened", "n_kept", "notes"]
DATE = "2026-11-06"
S2 = "https://api.semanticscholar.org/graph/v1"
CF = "fields=title,externalIds,year,venue,publicationDate,abstract,contexts,intents,authors&limit=1000 (offset paging)"

# n_screened, n_kept, notes per raw file (relative to raw/citations); kept = rated background or above, new to known_papers.csv
SCREEN = {}


def s(rel, screened, kept, notes):
    SCREEN[rel] = (screened, kept, notes)


rows = []


def n_from(rel):
    p = os.path.join(RAW, rel)
    if os.path.exists(p):
        if rel.endswith(".json"):
            js = json.load(open(p))
            if isinstance(js, dict) and "pages" in js:
                return str(js["n"])
            if isinstance(js, dict) and "meta" in js:
                if "reftitle_" in rel or "search_" in rel:
                    return str(len(js.get("results", [])))  # title lookups: records returned, not total hits
                return str(js["meta"].get("count"))
            if isinstance(js, list):
                return str(len(js))
            if isinstance(js, dict) and "data" in js:
                return str(len(js["data"]))
            return "1"
        if rel.endswith(".xml"):
            root = ET.parse(p).getroot()
            ns = {"os": "http://a9.com/-/spec/opensearch/1.1/"}
            t = root.find("os:totalResults", ns)
            return t.text if t is not None else "?"
        return "-"
    for suf in (".err", ".partial"):
        if os.path.exists(p + suf):
            return "failed"
    return "not run"


def add(database, query, filters, rel, screened="", kept="", notes=""):
    n = n_from(rel) if rel else "-"
    if n == "not run":
        return  # only queries actually run are logged
    if rel in SCREEN:
        screened, kept, extra = SCREEN[rel]
        notes = (notes + " " + extra).strip()
    if n == "failed":
        errp = os.path.join(RAW, rel + ".err")
        head = open(errp, "rb").read(40).decode("utf-8", "replace").split("\n")[0] if os.path.exists(errp) else ""
        notes = (f"FAILED ({head}) after 5 retries with 60 s waits. " + notes).strip()
        screened, kept = "0", "0"
    rows.append(dict(zip(COLS, [DATE, database, query, filters, n, screened, kept, notes])))


# ------------------------------------------------------------------ screening counts (hand-entered)
s("s2/cit_2412.06559.json", "362", "16",
  "All 362 titles and 258 citation contexts screened; abstracts read for the 50 matching the keyword list (false positive/alarm/negative/reject, over-critic, specificity, criterion, threshold, base rate, framing, strict, lenient, calibration, signal detection) and about 30 more picked by title. Kept 3 related (2601.14691, 2609.00038, 2610.06668) and 13 background; 2608.16003 and 2605.20745 already known.")
s("openalex/cites_2412.06559.json", "79", "2",
  "55 overlap the S2 list; the 24 OpenAlex-only titles screened (several are venue versions of S2 entries); kept 2 background (AAAI 2026: Rectify Evaluation Preference; FindTheFlaws); also gave the EMNLP 2026 Findings venue of 2601.14691.")
s("s2/cit_2601.13537.json", "11", "4", "Kept 2606.30587 (close), 2609.27756 (related), 2605.28188 and a bachelor thesis (background); 7 excluded.")
s("openalex/cites_2601.13537.json", "3", "1", "2 overlap S2 (excluded); kept RecSys 2026 anchoring-bias paper (background).")
s("s2/cit_2603.14893.json", "8", "6", "Kept 2610.15415, 2606.15610, 2603.25112 (related) and 2610.06522, 2607.11881, 2605.06673 (background); 2608.16003 known; one duplicate DOI record of 2606.15610.")
s("openalex/cites_2603.14893.json", "0", "0", "")
s("s2/cit_2608.16003.json", "0", "0", "S2 citationCount 0.")
s("openalex/cites_2608.16003.json", "0", "0", "")
s("openalex/cites_2609.18204.json", "0", "0", "")
s("s2/cit_2609.18204.json", "1", "1", "Succeeded on the second pass. One citer (2610.30882, background).")
s("s2/cit_2610.22631.json", "0", "0", "Posted Oct 15, 2026.")
s("openalex/cites_2610.22631.json", "0", "0", "")
s("openalex/cites_2609.09703.json", "0", "0", "")
s("s2/cit_2603.00539.json", "10", "2", "Succeeded on the second pass. Kept 2 background (2610.36010, 2607.21656); 2608.16003 known; 7 excluded.")
s("openalex/cites_2603.00539.json", "7", "2", "Kept 2 background (MDPI AI code self-refinement regressions; EMNLP 2026 Findings COVERA); 5 excluded.")
s("openalex/cites_2604.15224.json", "0", "0", "")
s("s2/cit_2605.20745.json", "4", "1", "Kept 2608.23941 (related); 2608.16003 known; 2 excluded.")
s("openalex/cites_2605.20745.json", "0", "0", "")
s("s2/ref_2608.16003.json", "22", "0", "Same items as the arXiv HTML list plus 5 parse fragments; nothing new.")
s("arxiv/html_2608.16003.html", "19", "11", "References screened by title, abstracts read via OpenAlex for kept items; 7 already in known_papers.csv; Lu et al. 2021 out of window.")
s("s2/ref_2609.18204.json", "25", "0", "Matches the arXiv HTML list; nothing new.")
s("arxiv/html_2609.18204.html", "25", "10", "Kept LLM-judge bias, automation-bias and SDT-method references as background; IS/management references and the authors' own non-judge papers excluded.")
s("arxiv/html_2610.22631.html", "48", "12", "Kept 2 related (2508.07805, 2604.06756) and 10 background; benchmarks, model reports and persuasion-in-general papers excluded.")
s("s2/ref_2603.14893.json", "31", "0", "Same items as the arXiv HTML list; used to resolve IDs.")
s("arxiv/html_2603.14893.html", "30", "11", "Kept SDT/metacognition and LLM-confidence references as background; datasets, model cards and calibration surveys excluded.")
s("s2/ref_2601.13537.json", "32", "12", "Only source for this list (HTML has no bibliography). Kept 12 background (judge bias, prompt sensitivity, sycophancy); 2508.07805 counted under 2610.22631; human framing classics, datasets and model cards excluded.")
s("arxiv/html_2601.13537.html", "49", "0", "No rendered bibliography: 49 unresolved citation keys, used only to cross-check the S2 list.")
s("arxiv/html_2606.30587.html", "85", "13", "")


# ------------------------------------------------------------------ rows
SEEDS = ["2608.16003", "2609.18204", "2610.22631", "2609.28564", "2609.09703", "2601.13537",
         "2603.00539", "2604.15224", "2605.20745", "2603.14893", "2412.06559"]


def main():
    add("Semantic Scholar Graph API", f"POST {S2}/paper/batch (27 known_papers arXiv ids)",
        "fields=title,year,venue,publicationDate,externalIds,citationCount,referenceCount,authors,abstract", "s2/known_batch.json",
        "0", "0", "Metadata, author ids and citation counts for the known papers.")
    oa_ids = {}
    for sd in SEEDS:
        p = os.path.join(RAW, f"openalex/work_{sd}.json")
        if os.path.exists(p):
            oa_ids[sd] = json.load(open(p))["id"].rsplit("/", 1)[1]
    for sd in SEEDS:
        add("Semantic Scholar Graph API", f"GET {S2}/paper/arXiv:{sd}/citations", CF,
            f"s2/cit_{sd}.json", notes="Forward citations.")
        if sd in oa_ids:
            add("OpenAlex", f"GET https://api.openalex.org/works?filter=cites:{oa_ids[sd]}", "per-page=200; no mailto",
                f"openalex/cites_{sd}.json", notes="Forward citations (fallback / cross-check).")
        else:
            add("OpenAlex", f"GET https://api.openalex.org/works/doi:10.48550/arXiv.{sd}", "", f"openalex/work_{sd}.json",
                "0", "0", "Work not found (404), so no cites: query possible.")
    for sd in ["2608.16003", "2609.18204", "2610.22631", "2603.14893", "2601.13537"]:
        add("Semantic Scholar Graph API", f"GET {S2}/paper/arXiv:{sd}/references", CF, f"s2/ref_{sd}.json",
            notes="Backward citations.")
        add("arXiv (HTML full text)", f"GET https://arxiv.org/html/{sd}", "reference section parsed", f"arxiv/html_{sd}.html",
            notes="Backward citations from the paper's own bibliography.")
    add("OpenAlex", "GET works/doi:10.48550/arXiv.<id> for 11 seed papers", "", "", "11", "0",
        "Resolved 10 OpenAlex work ids (2609.28564 not indexed).")
    add("OpenAlex", "GET works?search=ProcessBench identifying process errors mathematical reasoning", "", "openalex/search_processbench.json",
        "25", "0", "Checked for a separate arXiv record of ProcessBench: only the ACL record (W4412886965) has citations.")
    # reference title lookups
    titles = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "citations_ref_titles.tsv"))]
    for i, (src, t) in enumerate(titles):
        rel = f"openalex/reftitle_{i:02d}.json"
        if not os.path.exists(os.path.join(RAW, rel)) and not os.path.exists(os.path.join(RAW, rel + ".err")):
            continue
        add("OpenAlex", f"GET works?search={t}", "per-page=3", rel, "3", "0" if i == 11 else "1",
            f"Abstract lookup for a reference of {src}." + (" Best match was a different paper." if i == 11 else ""))
    # authors
    names = ["Parsa Mazaheri", "Kasra Mazaheri", "Zihan Chen", "Di Zhu", "Lei Zheng", "Weiling Li",
             "Anglin Cai", "Zhiqi Wang", "Xiaozhi Yang", "Yurun Lin", "Dongwon Lee", "Yuchen Yang",
             "Jon-Paul Cacioli", "Yerin Hwang", "Dongryeol Lee", "Taegwan Kang", "Minwoo Lee", "Kyomin Jung"]
    AU = {}  # n_kept per author for arXiv queries (hand-entered below)
    AU.update({"Parsa Mazaheri": ("5", "0"), "Kasra Mazaheri": ("3", "0"), "Zihan Chen": ("76", "0"), "Di Zhu": ("44", "0"),
               "Lei Zheng": ("39", "0"), "Weiling Li": ("5", "0"), "Anglin Cai": ("1", "0"), "Zhiqi Wang": ("11", "0"),
               "Xiaozhi Yang": ("1", "0"), "Yurun Lin": ("1", "0"), "Dongwon Lee": ("47", "0"), "Yuchen Yang": ("67", "0"),
               "Jon-Paul Cacioli": ("21", "3"), "Yerin Hwang": ("7", "4"), "Dongryeol Lee": ("8", "0"), "Taegwan Kang": ("6", "0"),
               "Minwoo Lee": ("12", "0"), "Kyomin Jung": ("34", "0")})
    for n in names:
        slug = n.replace(" ", "_")
        q = f'au:"{n}" AND submittedDate:[202501010000 TO 202611062359]'
        sc, kp = AU[n]
        add("arXiv API", f"search_query={q}", "sortBy=submittedDate; max_results=300", f"arxiv/au_{slug}.xml", sc, kp,
            "All titles screened; namesakes excluded by co-authors and topic. Papers kept under one author are not recounted under co-authors.")
    for f in sorted(glob.glob(os.path.join(RAW, "openalex/authorworks_*_A*.json"))):
        rel = os.path.relpath(f, RAW)
        m = re.match(r"openalex/authorworks_(.+)_(A\d+)\.json", rel)
        add("OpenAlex", f"GET works?filter=author.id:{m.group(2)},from_publication_date:2025-01-01 ({m.group(1).replace('_', ' ')})",
            "per-page=200", rel, "", "", "Titles screened; overlaps the arXiv author query except OSF/Zenodo and venue records.")
    add("OpenAlex", "GET works?filter=author.id:A5065892263,from_publication_date:2025-01-01 (Cacioli, with abstracts)", "per-page=200",
        "openalex/authorworks_abs_Cacioli.json", "77", "3", "OSF/Zenodo registrations and reports; kept 3 background (thinking-mode confidence, faithfulness-judge confidence, know-say gap).")
    for f in sorted(glob.glob(os.path.join(RAW, "dblp/author_search_*.json*"))):
        rel = os.path.relpath(f, RAW).replace(".err", "")
        nm = re.sub(r"^dblp/author_search_|\.json$", "", rel).replace("_", " ")
        add("DBLP search API", f"GET https://dblp.org/search/author/api?q={nm}", "format=json; h=50", rel, "0", "0",
            "Bot-check page (Anubis, HTTP 202) or 429; DBLP abandoned.")
    for f in sorted(glob.glob(os.path.join(RAW, "s2/author_*"))):
        rel = os.path.relpath(f, RAW).replace(".err", "").replace(".partial", "")
        if rel in [r.get("_rel") for r in rows]:
            continue
        m = re.match(r"s2/author_(.+)_(\d+)\.json", rel)
        if not m:
            continue
        add("Semantic Scholar Graph API", f"GET {S2}/author/{m.group(2)}/papers ({m.group(1).replace('_', ' ')})",
            "fields=title,externalIds,year,venue,publicationDate&limit=1000", rel, "", "0", "2025-26 titles screened; same 2609.18204-group papers as the arXiv author query (plus namesake items); nothing new kept.")
    # full texts and metadata
    for sd in ["2606.30587", "2609.27756", "2610.15415", "2606.15610", "2609.00038", "2603.18740"]:
        if sd == "2606.30587":
            continue  # logged with its reference count via SCREEN
        add("arXiv (HTML full text)", f"GET https://arxiv.org/html/{sd}", "", f"arxiv/html_{sd}.html", "1", "1",
            "Full-text read of a candidate.")
    add("arXiv (HTML full text)", "GET https://arxiv.org/html/2606.30587", "reference section parsed", "arxiv/html_2606.30587.html",
        "85", "13", "Second hop (close paper): full text read and 85 references screened by title; kept 13 background references.")
    add("arXiv API", "id_list=<27 known_papers ids>", "max_results=50", "arxiv/known_idlist.xml", "27", "0",
        "Versions and comments of known papers (no new versions of the five seeds).")
    add("arXiv API", "id_list=<52 screened arXiv ids>", "max_results=100", "arxiv/screened_idlist.xml", "52", "0",
        "Authors, versions and venue comments for screened papers.")
    add("arXiv API", "id_list=<25 more screened arXiv ids>", "max_results=50", "arxiv/screened_idlist2.xml", "25", "0",
        "Authors, abstracts and venue comments for references and citers added later.")
    add("arXiv API", "id_list=<11 third-hop arXiv ids>", "max_results=20", "arxiv/screened_idlist3.xml", "11", "0",
        "Abstracts and metadata for third-hop candidates.")
    add("arXiv API", 'search_query=abs:"confirmation bias" AND abs:vulnerability AND submittedDate:[202501010000 TO 202611062359]', "max_results=50",
        "arxiv/search_confirmation_bias_vuln.xml", "7", "0", "Attempt to locate the He et al. (2026) paper cited in 2605.23243; not found.")
    # later hops: forward citations and full texts
    HOPS = {"2606.30587": ("second hop (close paper)", "1", "1", "Only citer 2610.32876, rated close."),
            "2610.32876": ("second hop (close paper)", "1", "1", "Only citer 2611.01311, rated related."),
            "2603.18740": ("third hop (close paper)", "8", "7", "Kept 2610.35942 (close), 2606.13757 (related), 2605.23243, 2610.33509, 2610.05399 (background); 2610.32876 and 2607.24964 counted elsewhere; 1 excluded."),
            "2610.35942": ("fourth hop (close paper)", "0", "0", "No citers yet.")}
    for sd, (lab, sc, kp, nt) in HOPS.items():
        add("Semantic Scholar Graph API", f"GET {S2}/paper/arXiv:{sd}/citations", CF, f"s2/cit_{sd}.json", sc, kp, f"Forward citations, {lab}. {nt}")
    for sd, sc, kp, nt in [("2610.32876", "71", "9", "Second hop: references screened by title; abstracts via arXiv API for arXiv items."),
                           ("2603.18740", "62", "4", "Third hop: references screened by title."),
                           ("2610.35942", "47", "7", "Fourth hop: references screened by title; kept Kapetanovic et al. (related), FinVerBench, Kumar et al., Huang et al., Sorkin & Woods 1985, Wolfe et al. 2005 (background) and 2603.18740 (close, counted elsewhere)."),
                           ("2611.01311", "-", "1", "Full text partly read (related)."),
                           ("2605.23243", "20", "0", "Reference list checked for the He et al. (2026) citation; not listed."),
                           ("2610.34151", "1", "1", "Full text read (related).")]:
        add("arXiv (HTML full text)", f"GET https://arxiv.org/html/{sd}", "", f"arxiv/html_{sd}.html", sc, kp, nt)
    add("Semantic Scholar Graph API", f"GET {S2}/paper/search?query=confirmation bias LLM vulnerability detection benign framing", "limit=20",
        "s2/search_confirmation_bias_vuln.json", "", "", "Attempt to locate the He et al. (2026) paper cited in 2605.23243.")
    for key in ["koo2024", "chen2024threshold", "bernstein2026", "thornton2026", "vasu2025", "jones2022", "itzhak2024", "echterhoff2024", "unitverif"]:
        rel = f"s2/match_{key}.json"
        add("Semantic Scholar Graph API", f"GET {S2}/paper/search/match?query=<title of {key}>", "fields=title,externalIds,year,venue,abstract,authors",
            rel, "1", "1", "Abstract lookup for a second-hop reference of 2606.30587 (or one citer).")
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            if r["n_screened"] == "" and r["n_results"].isdigit():
                r["n_screened"] = r["n_results"]  # every returned record was screened by title
            if r["n_kept"] == "":
                r["n_kept"] = "0"
            w.writerow({k: r[k] for k in COLS})
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
