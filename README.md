# rel_coref_experiments

This repository contains some scripts to run experiments on different options of coreference search in REL, and to evaluate the results in a notebook and a report.
Experiments are run both on the AIDA data and on the msmarco data. 


## Setup

### Data

The data directory stores necessary inputs and outputs from the scripts below. The directory should have the following structure:

```
data
|___ ed-wiki-2019
    |   ...
|___ generic
    |   ...
|___ wiki_2019
    |   ...
|___ msmarco
    |   sample_1k_longdocs.parquet
    |   sample_1k_longdocs.gz
|___ efficiency_test
```

Details:
- `ed-wiki-2019`, `generic`, `wiki_2019`: standard data also used in REL. for downloading them, see the `REL/scripts/download_data.sh`
- msmarco contains the following files I obtained from Chris:
    - file with mentions (`sample_1k_longdocs.parquet`) 
    - source file (`sample_1k_longdocs.gz`)
- The empty `efficiency_test` where output from `REL/scripts/run_efficiency_tests.sh` (currently in [PR](https://github.com/informagi/REL/pull/153)) is stored.


### Software

Now install the relevant software. Because of some conflicting pythonr requirements, two conda environments are necessary:
- `env_rebl`: for running the batch ED with REBL
- `rel`: for running efficiency test scripts in REL

```bash
cd some_empty_directory

# Install
# when PR https://github.com/informagi/REL/pull/153 is merged, clone REL directly
git clone -b flavio/coref-lsh git@github.com:f-hafner/REL.git 
git clone -b lsh-integration git@github.com:informagi/REBL.git 
git clone git@github.com:f-hafner/rebl_coref.git # TODO: change name

# set up environment for REBL
cd rebl_coref # TODO: change name
conda activate 
conda env create --prefix ./env --file environment.yml

conda activate ./env
pip install ../REBL/
pip install -e ../REL/.

# Set up environment for REL
conda deactivate
conda create -n rel python=3.7 # TODO: transform this into an environment as env_rebl above?
conda activate rel
pip install -e REL/.[develop]

```


## Running experiments

```bash
BASE_URL="path/to/data/directory" # replace here the URL to the data. for me: "/var/scratch/fhafner/rel_data/"

# # 1.Run REBL
conda activate 
conda activate ./env_rebl
bash pipeline.sh $BASE_URL

conda activate ./env_rel
cd ../REL/
# # 2. Run efficiency tests
bash scripts/run_efficiency_tests.sh $BASE_URL # change directory and settings in REL/scripts/efficiency_test.py. or change code in PR? 
```

Details 
- both `pipeline.sh` and `REL/scripts/run_efficiency_tests.sh` need one argument that indicates the directory to the data 
- `pipeline.sh` contains other variables, but they do not need to be changed: `COREF_OPTIONS`, `NDOCS_TIMING`


## Looking at the data

1. The notebook `analysis.ipynb` collects the data from the experiments above, evaluates predictions and makes some plots. 
    - update the path to the data in the first cell 
2. Everything is then also discussed in text form in /tex/coreferes.tex. The data in the tables are not automatically updated.

XXX: need also environment for the notebook! 
XXX: add also the script for checking the lsh performance?