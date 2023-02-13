# rebl_coref
Use REBL with development version of REL for coref



# use conda environment, development version of REL, and changed version of REBL in local folder. ie: 
# activate conda ./env; pip install ../REBL/.; pip install -e ../REL/.
    # try to change this to use my REL fork in the requirements


# this is not necessary, the input file for the next step is already available 
# python -m rebl.md.mention_detection \
#     --in_file "../data/msmarco/msmarco_doc_00_5k.gz" \
#     --out_file "output/md.parquet" 

# pip install ../REBL/.
# pip install -e ../REL/.
