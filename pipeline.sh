#!/bin/bash

# use conda environment, development version of REL, and changed version of REBL in local folder. ie: 
# activate conda ./env; pip install ../REBL/.; pip install -e ../REL/.
    # try to change this to use my REL fork in the requirements


# this is not necessary, the input file for the next step is already available 
# python -m rebl.md.mention_detection \
#     --in_file "../data/msmarco/msmarco_doc_00_5k.gz" \
#     --out_file "output/md.parquet" 

# pip install ../REBL/.
# pip install -e ../REL/.

# ## Effectiveness: use the batch disambiguation

# run ED with different coref options 
MDFILE="/var/scratch/fhafner/rel_data/msmarco/sample_1k_longdocs.parquet"
SOURCEFILE="/var/scratch/fhafner/rel_data/msmarco/sample_1k_longdocs.gz"
URL="/var/scratch/fhafner/rel_data/"

python3 -m rebl.ed.entity_disambiguation \
    --md_file $MDFILE  \
    --fields title headings body \
    --source_file $SOURCEFILE \
    --out_file /var/scratch/fhafner/rel_data/msmarco/predictions/ed_coref_all.parquet \
    --base_url $URL \
    --wiki_version wiki_2019 \
    --identifier docid \
    --search_corefs "all" \
    &> ed_coref_all.log

python3 -m rebl.ed.entity_disambiguation \
    --md_file $MDFILE \
    --fields title headings body \
    --source_file $SOURCEFILE \
    --out_file /var/scratch/fhafner/rel_data/msmarco/predictions/ed_coref_lsh.parquet \
    --base_url $URL \
    --wiki_version wiki_2019 \
    --identifier docid \
    --search_corefs "lsh" \
    &> ed_coref_lsh.log

python3 -m rebl.ed.entity_disambiguation \
    --md_file $MDFILE  \
    --fields title headings body \
    --source_file $SOURCEFILE \
    --out_file /var/scratch/fhafner/rel_data/msmarco/predictions/ed_coref_off.parquet \
    --base_url $URL \
    --wiki_version wiki_2019 \
    --identifier docid \
    --search_corefs "off" \
    &> ed_coref_off.log


# ## Efficiency: disambiguate by document 
python3 msmarco_timing.py --n_docs 1000 --search_corefs "all" &> timing_ed_coref_all.log
python3 msmarco_timing.py --n_docs 1000 --search_corefs "lsh" &> timing_ed_coref_lsh.log
python3 msmarco_timing.py --n_docs 1000 --search_corefs "off" &> timing_ed_coref_off.log


# python3 msmarco_largedoc_memory.py --n_docs 5000 --search_corefs "lsh" 