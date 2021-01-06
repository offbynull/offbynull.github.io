TYPE="anki"
mkdir -p /opt/$TYPE
rm -rf /opt/$TYPE/*
cp /input/anki_js/dist/anki.js /opt/$TYPE 
cp /input/anki_js/dist/anki.js.map /opt/$TYPE 
echo "[ [\"anki.js\", \"anki.js.map\"] ]" >> /output/output.injects