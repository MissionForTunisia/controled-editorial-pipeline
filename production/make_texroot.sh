#!/bin/bash
# make_texroot.sh — assemble un arbre TEXMF minimal + pdflatex fonctionnel
# à partir du clone texmf-dist et du pdftex fraîchement compilé.
set -e

SRC=/tmp/tl/src/texlive-source-trunk
TEXMF=/tmp/tl/texmf-dist
INST=/tmp/tl/inst
ROOT=/tmp/tl/texroot

rm -rf "$ROOT"
mkdir -p "$ROOT/bin" "$ROOT/texmf/web2c" "$ROOT/texmf/fonts/map/pdftex/updmap"

# 1) binaires
cp "$INST"/bin/pdftex "$ROOT/bin/" 2>/dev/null || cp "$(find /tmp/tl/build -name pdftex -type f -perm -u+x | head -1)" "$ROOT/bin/"
for n in pdflatex latex initex texconfig; do ln -sf pdftex "$ROOT/bin/$n"; done

# 2) kpathsea runtime config
cat > "$ROOT/texmf/web2c/texmf.cnf" <<'EOF'
TEXMFROOT = /tmp/tl/texroot
TEXMF = {!!$TEXMFROOT/texmf, !!$TEXMFROOT/texmf-dist}
TEXMFDBS = $TEXMF
SYSTEXMF = $TEXMF
TEXFORMATS = $TEXMFROOT/texmf/web2c/$engine
TEXFONTMAPS = .;$TEXMF/fonts/map/{$engine,dvips,}//
ENCFONTS = .;$TEXMF/fonts/enc//
TFMFONTS = .;$TEXMF/fonts/tfm//{$engine,}//
VFFONTS = .;$TEXMF/fonts/vf//
TYPE1FONTS = .;$TEXMF/fonts/type1//
TEXINPUTS.pdflatex = .;$TEXMF/tex/{latex,generic,plain}//
TEXINPUTS.latex = .;$TEXMF/tex/{latex,generic,plain}//
TEXINPUTS.initex = .;$TEXMF/tex/{latex,generic,plain}//
TEXPSHEADERS = .;$TEXMF/dvips//;$TEXMF/fonts/type1//
OSFONTDIR =
TEXCONFIG = $TEXMF/dvips
MAX_PRINT_LINE = 10000
error_line = 79
half_error_line = 50
save_size = 5000000
main_memory = 12000000
font_mem_size = 8000000
pool_size = 8000000
string_vacancies = 300000
max_strings = 600000
strings_free = 3000
nest_size = 500
param_size = 10000
break_size = 10000
eq_tb_size = 200000
eqt_size = 20000
hash_extra = 200000
buf_size = 200000
font_max = 9000
max_font_id = 9000
expand_depth = 10000
EOF

# 3) base de données de fichiers (ls-R)
( cd "$TEXMF" && ls -R . > "$ROOT/texmf/ls-R" ) >/dev/null 2>&1 || true
( cd "$ROOT/texmf" && find . -maxdepth 2 | sort > ls-R.local )
cat "$ROOT/texmf/ls-R.local" "$ROOT/texmf/ls-R" > /tmp/lsR.merged && mv /tmp/lsR.merged "$ROOT/texmf/ls-R"
rm -f "$ROOT/texmf/ls-R.local"

# 4) carte des fontes : lm + cm (concaténation des fragments dvips)
( cd "$TEXMF/fonts/map/dvips"
  cat lm/lm.map lm/lm-ec.map cm/cmtext-bsr-interpolated.map fira/fira.map 2>/dev/null || true
) > "$ROOT/texmf/fonts/map/pdftex/updmap/pdftex.map"

# 5) language.dat pour la construction du format
cp "$TEXMF/tex/generic/config/language.dat" "$ROOT/texmf/web2c/language.dat"
cp "$TEXMF/tex/generic/config/language.def" "$ROOT/texmf/web2c/language.def" 2>/dev/null || true

echo "TEXROOT prêt : $ROOT"
ls -la "$ROOT/bin"
