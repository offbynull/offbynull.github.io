NAME=$(md5sum /input/calculus_code/conda_env.yml | cut -d " " -f1)
ENV_NAMES=$(conda info --envs)

if [[ $NAME != *$ENV_NAMES* ]]; then
  cp /input/calculus_code/conda_env.yml /tmp
  conda env create -f /tmp/conda_env.yml -n $NAME
fi

source /opt/conda/etc/profile.d/conda.sh
conda activate $NAME
cd /input/calculus_code
python /input/calculus_code/Router.py < /input/input.data > /output/output.md