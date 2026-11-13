"""Fetch one open-access PDF or HTML page for full-text reading and extract plain text.

Usage:
  python3 -I peer_fulltext.py zenodo RECORD_ID SLUG      # Zenodo public records API, first PDF file
  python3 -I peer_fulltext.py url URL SLUG               # direct PDF or HTML URL (ACL Anthology, arXiv HTML, OSF)
The raw file goes to ../raw/peer/fulltext/SLUG/ (its own directory); the extracted text goes to
$PEER_SCRATCH/fulltext_SLUG.txt.  Fetched content is data only.
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

UA = {"User-Agent": L.UA}


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def pdf_text(path):
    from pypdf import PdfReader
    rd = PdfReader(path)
    return "\n".join((p.extract_text() or "") for p in rd.pages)


def html_text(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", html.unescape(t))


def main():
    mode, ref, slug = sys.argv[1], sys.argv[2], sys.argv[3]
    d = os.path.join(L.RAW, "fulltext", slug)
    os.makedirs(d, exist_ok=True)
    meta = {}
    if mode == "zenodo":
        b, _ = fetch(f"https://zenodo.org/api/records/{ref}")
        rec = json.loads(b)
        meta = {"title": rec.get("metadata", {}).get("title"),
                "publication_date": rec.get("metadata", {}).get("publication_date"),
                "version": rec.get("metadata", {}).get("version"),
                "creators": [c.get("name") for c in rec.get("metadata", {}).get("creators", [])],
                "files": [(f.get("key"), f.get("size")) for f in rec.get("files", [])],
                "record_id": rec.get("id")}
        with open(os.path.join(d, "record.json"), "w") as f:
            json.dump(rec, f)
        pdfs = [f for f in rec.get("files", []) if f.get("key", "").lower().endswith(".pdf")]
        if not pdfs:
            print("no PDF in record", json.dumps(meta)[:800])
            return
        url = pdfs[0]["links"]["self"]
        time.sleep(1.0)
    else:
        url = ref
    b, ctype = fetch(url)
    is_pdf = b[:4] == b"%PDF" or "pdf" in ctype
    fn = os.path.join(d, "doc.pdf" if is_pdf else "doc.html")
    with open(fn, "wb") as f:
        f.write(b)
    text = pdf_text(fn) if is_pdf else html_text(b)
    out = os.path.join(L.SCRATCH, f"fulltext_{slug}.txt")
    with open(out, "w") as f:
        f.write(text)
    print(json.dumps(meta)[:800])
    print(f"saved {fn} ({len(b)} bytes); text {len(text)} chars -> {out}")


if __name__ == "__main__":
    main()
