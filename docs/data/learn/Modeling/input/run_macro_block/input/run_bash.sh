NAME=$(md5sum /input/conda_env.yml | cut -d " " -f1)
ENV_NAMES=$(conda info --envs)

if [[ $NAME != *$ENV_NAMES* ]]; then
  cp /input/conda_env.yml /tmp
  conda env create -f /tmp/conda_env.yml -n $NAME
fi

# https://stackoverflow.com/a/821419
set -e

grep -v '^#>>>' /input/input.data > /tmp/input.data

source /opt/conda/etc/profile.d/conda.sh
conda activate $NAME
cd /input
echo "`{bm-disable-all}`" > /output/output.md 
python /input/output.py < /tmp/input.data >> /output/output.md
echo "<div style=\"border:1px solid black;\">" >> /output/output.md 
python /tmp/input.data >> /output/output.md
echo "</div>" >> /output/output.md 
echo "`{bm-enable-all}`" >> /output/output.md 