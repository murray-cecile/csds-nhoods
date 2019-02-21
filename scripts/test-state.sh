#!/bin/bash 

echo "Arguments :: "$@

set -e

echo "unsetting ids"
unset SUDO_UID SUDO_GID SUDO_USER

echo "setting minidir"
if [ -z "$OSG_WN_TMP" ]; then 
  minidir=`mktemp -d`
else 
  minidir=`mktemp -d -p $OSG_WN_TMP`
fi

echo "setting home"
export HOME=${minidir}

echo "setting condarc"
cat condarc | sed "s|XYZ|$minidir|" > tmp_conda
mv tmp_conda condarc
export CONDARC=$(pwd)/condarc

echo "making condarc"
bash miniconda.sh -b -p ${minidir}/miniconda

export PATH="${minidir}/miniconda/bin:$PATH"


# source $minidir/miniconda/bin/activate

echo "installing geopandas"
conda install -y geopandas 

python --version
which python
python process_single_job.py -j $1 -st $2

ls *
