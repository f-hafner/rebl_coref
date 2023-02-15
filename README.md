# rebl_coref
The scripts in this repo run some experiments of REL with the msmarco data.

# TODO
- add parts on running efficiency_tests from REL, and on evaluation? 

## Usage
```bash
cd some_empty_directory

# Install
# when PR https://github.com/informagi/REL/pull/153 is merged, clone REL directly
git clone -b flavio/coref-lsh git@github.com:f-hafner/REL.git 
git clone -b lsh-integration git@github.com:informagi/REBL.git 
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

The `DATA_URL` is the location of all the data needed, and also where the output data is stored. It should have the following structure
```
DATA_URL
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
- ed-wiki-2019, generic, wiki_2019: standard data also used in REL. for downloading them, see the `REL/scripts/download_data.sh`
- msmarco contains the following files I obtained from Chris:
    - file with mentions (`sample_1k_longdocs.parquet`) 
    - source file (`sample_1k_longdocs.gz`)
- The empty `efficiency_test` where output from `REL/scripts/run_efficiency_tests.sh` (currently in [PR](https://github.com/informagi/REL/pull/153)) is stored.

Moreover, the `pipeline.sh` writes the output data to subdirectories in `DATA_URL/msmarco?`. If the directories do not exist, they are created. 

XXX: what to put in there before? efficiency_test is needed not here, but in REL/scripts. combine all in one? rename the directory/repository?
