#!/bin/bash
# bootstrap.sh — reconstruit toute la chaîne TeX minimale depuis les sources.
# Usage : production/bootstrap.sh
# Étapes : téléchargement texlive-source + texmf-dist (miroir GitHub) →
#          compilation pdfLaTeX → assemblage TEXMFROOT → format pdflatex.
set -e
ROOTDIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p /tmp/tl/src
cd /tmp/tl/src
if [ ! -d texlive-source-trunk ]; then
  echo ">> téléchargement texlive-source…"
  curl -sL --retry 3 -o texlive-source.tar.gz \
    https://codeload.github.com/TeX-Live/texlive-source/tar.gz/refs/heads/trunk
  tar xzf texlive-source.tar.gz
fi

if [ ! -d /tmp/tl/texmf-dist/tex/latex ]; then
  echo ">> clonage sparse du texmf-dist…"
  cd /tmp/tl
  git clone --no-checkout --depth 1 --filter=blob:none \
    https://github.com/SachaNevsky/latexdiff-texmf-dist.git texmf-dist
  cd texmf-dist
  git sparse-checkout init --no-cone
  printf '/tex/latex/**\n/tex/generic/**\n/tex/plain/**\n/fonts/enc/**\n/fonts/map/**\n/fonts/tfm/public/**\n/fonts/vf/**\n/fonts/type1/**\n/dvips/**\n/web2c/**\n/scripts/texlive/**\n/bibtex/**\n' > .git/info/sparse-checkout
  git checkout
fi

echo ">> configuration + compilation de pdftex (2 cœurs)…"
mkdir -p /tmp/tl/build
cd /tmp/tl/build
/tmp/tl/src/texlive-source-trunk/configure \
  --disable-native-texlive-build --disable-all-pkgs \
  --enable-web2c --enable-pdftex --without-x --prefix=/tmp/tl/inst
make -j2
make install

echo ">> assemblage du TEXMFROOT…"
"$ROOTDIR/production/make_texroot.sh"

echo ">> construction du format pdflatex…"
export PATH=/tmp/tl/texroot/bin:$PATH
export TEXMFROOT=/tmp/tl/texroot
mkdir -p /tmp/tl/texroot/texmf/web2c
cd /tmp/tl/texroot/texmf/web2c
./../../bin/pdftex -ini -etex -jobname=pdflatex -progname=pdflatex pdflatex.ini >/dev/null
mv -f pdflatex.fmt /tmp/tl/texroot/texmf/web2c/pdflatex.fmt 2>/dev/null || true

echo ">> vérification…"
cd /tmp && printf '\\documentclass{article}\\begin{document}Bonjour.\\end{document}' > smoke.tex
/tmp/tl/texroot/bin/pdflatex -interaction=nonstopmode smoke.tex | tail -2
echo ">> bootstrap terminé."
