#!/usr/bin/env python3
"""Extract plain text from a PDF (untrusted data) with pypdf. Usage: python3 -I arxiv_pdftext.py <pdf> <out_txt>"""
import sys
from pypdf import PdfReader

r = PdfReader(sys.argv[1])
with open(sys.argv[2], "w", encoding="utf-8") as fh:
    for i, p in enumerate(r.pages):
        fh.write(f"\n=== page {i + 1} ===\n" + (p.extract_text() or ""))
print(len(r.pages), "pages")
