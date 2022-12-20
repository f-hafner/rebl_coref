

"Time the execution of ED with the msmarco data"

import json 
import pickle 
import pandas as pd
import time 
import argparse

from REL.entity_disambiguation import EntityDisambiguation
from REL.mention_detection import MentionDetection
from rebl.utils import input_stream_gen_lines


parser = argparse.ArgumentParser()
parser.add_argument( 
    "--no_corefs",
    action="store_true",
    help="use function with_coref()?", 
    default=False)

parser.add_argument( 
    "--n_docs",
    type=int,
    help="number of documents to process. Use 6000 to process all documents",
    default=2)


args = parser.parse_args()
print(f"args.no_corefs is {args.no_corefs}")


base_url = "/home/flavio/projects/rel20/data"
wiki_version = "wiki_2019" 
config = {
        "mode": "eval",
        "model_path": "{}/{}/generated/model".format(base_url, wiki_version),
    }

# Instantiate 
mention_detection = MentionDetection(base_url, wiki_version)
ed_model = EntityDisambiguation(base_url, wiki_version, config, reset_embeddings=True, no_corefs=args.no_corefs)

datapath = "../data/msmarco/"

d = pd.read_parquet(f"{datapath}msmarco_doc_md_00_5k.parquet")

# load the text file 
source_file = "../data/msmarco/msmarco_doc_00_5k.gz" 
stream_raw_source_file = input_stream_gen_lines(source_file) # one item = one document 


measurements = {}

## iterate over documents, run ED and save timing/number of mentions
for index, doc in zip(range(args.n_docs), stream_raw_source_file):
    json_content = json.loads(doc)
    # doc0 = next(stream_raw_source_file)
    # json_content = json.loads(doc0)

    # extract items for format_spans
    current_text = json_content["body"]

    docid = json_content["docid"]
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


filename = "ed_coref"
if args.no_corefs:
    filename = "ed_nocoref"

filename = f"{datapath}timing/{filename}_ndocs_{args.n_docs}"

with open(f"{filename}.pickle", "wb") as f:
    pickle.dump(measurements, f, protocol=pickle.HIGHEST_PROTOCOL)        


print("Done.")
