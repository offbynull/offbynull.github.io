NAME=fdp_$(md5sum < /input/input.data | cut -d " " -f1).svg
fdp -Tsvg /input/input.data > /output/$NAME
echo "![Fdp diagram]($NAME)" > /output/output.md