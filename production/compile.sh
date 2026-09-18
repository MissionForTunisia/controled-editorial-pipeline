#!/bin/bash
# compile.sh — compilation contrôlée du livre (3 passes pdfLaTeX)
# Usage : production/compile.sh [repertoire] [--once]
set -e
DIR="${1:-$HOME/controled-editorial-pipeline/book}"
PASSES=3
[ "${2:-}" = "--once" ] && PASSES=1

export TEXMFROOT=/tmp/tl/texroot
export PATH=/tmp/tl/texroot/bin:$PATH
export TEXINPUTS=".:/tmp/tl/texmf-dist/tex/latex//:/tmp/tl/texmf-dist/tex/generic//:/tmp/tl/texmf-dist/tex/plain//:$TEXMFROOT/texmf/tex//"
export TEXFONTMAPS=".:/tmp/tl/texmf-dist/fonts/map/dvips//:/tmp/tl/texmf-dist/fonts/map/pdftex//:$TEXMFROOT/texmf/fonts/map/pdftex/updmap//"
export ENCFONTS=".:/tmp/tl/texmf-dist/fonts/enc//"
export TFMFONTS=".:/tmp/tl/texmf-dist/fonts/tfm//"
export VFFONTS=".:/tmp/tl/texmf-dist/fonts/vf//"
export T1FONTS=".:/tmp/tl/texmf-dist/fonts/type1//"
export TYPE1FONTS="$T1FONTS"
export TEXPSHEADERS=".:/tmp/tl/texmf-dist/dvips//:/tmp/tl/texmf-dist/fonts/enc//"
export TEXFORMATS="$TEXMFROOT/texmf/web2c"

cd "$DIR"
for i in $(seq 1 $PASSES); do
  echo "== passe $i =="
  pdflatex -interaction=nonstopmode -halt-on-error main.tex | tail -3
done
echo "== terminé =="
pdfinfo main.pdf 2>/dev/null | grep -E "Pages|Page size" || python3 -c "import pymupdf; d=pymupdf.open('main.pdf'); print('Pages:', len(d))"
