#!/bin/bash

# Set parameters
DATA_URL="/var/scratch/fhafner/rel_data/"
COREF_OPTIONS=("all" "off" "lsh")
NDOCS_TIMING=1000

MDFILE="${DATA_URL}/msmarco/sample_1k_longdocs.parquet" # file with detected mentions
SOURCEFILE="${DATA_URL}/msmarco/sample_1k_longdocs.gz"

# some housecleaning
dirs_to_create=(logs "${DATA_URL}msmarco/predictions/" "${DATA_URL}msmarco/timing/")
for directory in ${dirs_to_create[@]}; do
    if [ ! -d $directory ]
    then 
        mkdir $directory 
    fi
done 

# Run 
for option in ${COREF_OPTIONS[@]}; do
    filename="ed_coref_${option}"
    logfile_ed="logs/${filename}.log"
    logfile_timing="logs/timing_${filename}.log"
    outfile="${DATA_URL}/msmarco/predictions/${filename}.log"

    # ## Effectiveness: use the batch disambiguation
    python -m rebl.ed.entity_disambiguation \
        --md_file $MDFILE  \
        --fields title headings body \
        --source_file $SOURCEFILE \
        --out_file $outfile \
        --base_url $DATA_URL \
        --wiki_version wiki_2019 \
        --identifier docid \
        --search_corefs $option \
        &> $logfile_ed
    
    # ## Efficiency: disambiguate by document 
    python msmarco_timing.py --n_docs $NDOCS_TIMING --search_corefs $option &> $logfile_timing
done 
