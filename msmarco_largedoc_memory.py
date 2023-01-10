

"Time the execution of ED with the msmarco data for a document with many mentions"

import json 
import pickle 
import pandas as pd
import time 
import argparse
import pdb 
import logging 

from REL.entity_disambiguation import EntityDisambiguation
from REL.mention_detection import MentionDetection
from rebl.utils import input_stream_gen_lines


parser = argparse.ArgumentParser()
parser.add_argument(
    '--search_corefs',
    type=str,
    choices=['all', 'lsh', 'off'],
    default='all',
    help="Setting for search_corefs in Entity Disambiguation."
)

parser.add_argument( 
    "--n_docs",
    type=int,
    help="number of documents to process. Use 6000 to process all documents",
    default=2)


args = parser.parse_args()
print(f"args.search_corefs is {args.search_corefs}")


base_url = "/home/flavio/projects/rel20/data"
wiki_version = "wiki_2019" 
config = {
        "mode": "eval",
        "model_path": "{}/{}/generated/model".format(base_url, wiki_version),
    }
keep_docid = "msmarco_doc_00_28953614" # main file to check (bit file with 15k mentions)
# keep_docid = "msmarco_doc_00_28495098" # try out
prep_file = False 
pickle_file = f"largedoc_{keep_docid}_mentions.pickle"

# logging.basicConfig(filename=f'logging_{keep_docid}.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG) # do not print to file 


# Instantiate 
mention_detection = MentionDetection(base_url, wiki_version)
ed_model = EntityDisambiguation(base_url, wiki_version, config, reset_embeddings=True, search_corefs=args.search_corefs)

datapath = "../data/msmarco/"

d = pd.read_parquet(f"{datapath}msmarco_doc_md_00_5k.parquet")

# load the text file 
source_file = "../data/msmarco/msmarco_doc_00_5k.gz" 
stream_raw_source_file = input_stream_gen_lines(source_file) # one item = one document 


measurements = {}


# extract the data for the relevant file 
if prep_file:
    print("preparing file with mention detection")
    for idx, doc in zip(range(args.n_docs), stream_raw_source_file):
        json_content = json.loads(doc)
        current_text = json_content["body"]
        docid = json_content["docid"]
        if docid != keep_docid:
            pass 
        elif docid == keep_docid:
            d_doc = d.loc[d["identifier"] == docid, :].copy()
            d_doc['length'] = d_doc["end_pos"] - d_doc["start_pos"]
            spans = list(d_doc.loc[:, ["start_pos", "length"]].to_records(index=False))
        
            processed = {f"{docid}": [current_text, spans]}
            # pdb.set_trace()
            mentions_dataset, total_ment = mention_detection.format_spans(processed)
            # save for later use 
            with open(pickle_file, "wb") as f:
                pickle.dump(mentions_dataset, f, protocol=pickle.HIGHEST_PROTOCOL)        

else:
    print("loading mentions from pickled file")
    with open(pickle_file, "rb") as file:
        mentions_dataset = pickle.load(file)


predictions, timing = ed_model.predict(mentions_dataset)


print("Done.")
