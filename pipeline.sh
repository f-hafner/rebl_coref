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

# run ED with and without coref 
# python3 -m rebl.ed.entity_disambiguation \
#     --md_file "../data/msmarco/msmarco_doc_md_00_5k.parquet" \
#     --fields title headings body \
#     --source_file "../data/msmarco/msmarco_doc_00_5k.gz" \
#     --out_file ../data/msmarco/predictions/ed_coref.parquet \
#     --base_url "/home/flavio/projects/rel20/data" \
#     --wiki_version wiki_2019 \
#     --identifier docid \
#     &> ed_coref.log

# python3 -m rebl.ed.entity_disambiguation \
#     --md_file "../data/msmarco/msmarco_doc_md_00_5k.parquet" \
#     --fields title headings body \
#     --source_file "../data/msmarco/msmarco_doc_00_5k.gz" \
#     --out_file ../data/msmarco/predictions/ed_nocoref.parquet \
#     --base_url "/home/flavio/projects/rel20/data" \
#     --wiki_version wiki_2019 \
#     --identifier docid \
#     --no_corefs \
#     &> ed_nocoref.log


# ## Efficiency: disambiguate by document 
python3 msmarco_timing.py --n_docs 1000 &> timing_ed_coref.log
python3 msmarco_timing.py --n_docs 1000 --no_corefs &> timing_ed_nocoref.log
