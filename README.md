# rebl_coref
The scripts in this repo run some experiments of REL with the msmarco data.


### TODO
- create necessary directories
- activate conda environment before running 


## Usage
```bash
cd some_empty_directory

# Install
# when PR https://github.com/informagi/REL/pull/153 is merged, clone REL directly
git clone -b flavio/coref-lsh git@github.com:f-hafner/REL.git 
git clone -b lsh-integration git@github.com:informagi/REBL.git # needs https://github.com/informagi/REBL/pull/8 to be merged
git clone git@github.com:f-hafner/rebl_coref.git

# set up environment
cd rebl_coref
conda activate 
conda env create --prefix ./env --file environment.yml

conda activate ./env
pip install ../REBL/
pip install -e ../REL/.

# Run 
bash pipeline.sh
```

The script `pipepline.sh` needs three main parameters:
- `DATA_URL`
- `COREF_OPTIONS`: the options to use for coreference search, according to the implementation in REL 
- `NDOCS_TIMING`: number of documents to process in the timing step 

The `DATA_URL` is the location of all the data needed, and also where the output data is stored:
- pre-existing directories: ed-wiki-2019, generic, wiki_2019. Download: see XXX
- create empty directories if they do not exist: msmarco, efficiency_test. XXX: what to put in there before? efficiency_test is needed not here, but in REL/scripts. combine all in one? rename the directory/repository?