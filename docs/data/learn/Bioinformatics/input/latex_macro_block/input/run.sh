NAME=latex_$(md5sum < /input/input.data | cut -d " " -f1).svg

mkdir -p /tmp/work
cd /tmp/work
cat /input/input.data > input.tex
latex input.tex
if [ ! $? -eq 0 ]; then
    exit 1
fi
dvisvgm input.dvi
if [ ! $? -eq 0 ]; then
    exit 1
fi
mv input-1.svg /output/$NAME
cd /
rm -rf /tmp/work

echo "![Latex diagram]($NAME)" > /output/output.md
