#!/bin/sh
# Build main.pdf with pdfLaTeX + BibTeX. The AAAI-27 style (aaai2027.sty) refuses XeLaTeX, LuaLaTeX and Tectonic.
# Uses pdflatex from PATH, or TinyTeX in ~/Library/TinyTeX when pdflatex is not on PATH.
# Intermediate files go to build/; the finished PDF is copied to main.pdf.
set -e
cd "$(dirname "$0")"
if ! command -v pdflatex >/dev/null 2>&1; then
    PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
fi
mkdir -p build
run() { pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex >build/pdflatex.out 2>&1 || { grep -n '^!' build/main.log; exit 1; }; }
run
(cd build && BIBINPUTS="..:" BSTINPUTS="..:" bibtex main >bibtex.out 2>&1) || { cat build/bibtex.out; exit 1; }
run
run
cp build/main.pdf main.pdf
grep -E 'LaTeX Warning|Overfull' build/main.log || true
grep -o -E 'Output written on [^ ]+ \([0-9]+ pages' build/main.log
