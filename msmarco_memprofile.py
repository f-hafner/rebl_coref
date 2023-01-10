

"Time the execution of ED with the msmarco data"

import json 
import pickle 
import pandas as pd
import time 
import argparse
from memory_profiler import profile 

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

# Instantiate 
mention_detection = MentionDetection(base_url, wiki_version)
ed_model = EntityDisambiguation(base_url, wiki_version, config, reset_embeddings=True, search_corefs=args.search_corefs)

datapath = "../data/msmarco/"

d = pd.read_parquet(f"{datapath}msmarco_doc_md_00_5k.parquet")

# load the text file 
source_file = "../data/msmarco/msmarco_doc_00_5k.gz" 
stream_raw_source_file = input_stream_gen_lines(source_file) # one item = one document 


measurements = {}

@profile 
def process_data():
    ## iterate over documents, run ED and save timing/number of mentions
    for idx, doc in zip(range(args.n_docs), stream_raw_source_file):
        print(f"idx is {idx}")
        if idx == 60: # program seems to get stuck 
            pass 
        else:
            json_content = json.loads(doc)
            # doc0 = next(stream_raw_source_file)
            # json_content = json.loads(doc0)

            # extract items for format_spans
            current_text = json_content["body"]

            docid = json_content["docid"]
            # print(f"docid is {docid}")
            d_doc = d.loc[d["identifier"] == docid, :].copy()
            d_doc['length'] = d_doc["end_pos"] - d_doc["start_pos"]
            spans = list(d_doc.loc[:, ["start_pos", "length"]].to_records(index=False))


            processed = {f"{docid}": [current_text, spans]}
            mentions_dataset, total_ment = mention_detection.format_spans(processed)
            
            start = time.time()
            predictions, timing = ed_model.predict(mentions_dataset)
            end = time.time()
            time_ed = end - start 

            out = {"n_mentions": total_ment, "timing_ed": time_ed}
            measurements[docid] = out

process_data()


print("Done.")
