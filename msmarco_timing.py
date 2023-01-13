

"Time the execution of ED with the msmarco data"

import json 
import pickle 
import pandas as pd
import time 
import argparse
import pdb 


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
run_files = False


## iterate over documents, run ED and save timing/number of mentions
for idx, doc in zip(range(args.n_docs), stream_raw_source_file):
    json_content = json.loads(doc)

    # extract items for format_spans
    current_text = json_content["body"]

    docid = json_content["docid"]
    # if docid == "msmarco_doc_00_28937045": # only run after this file was seen. when using flush: msmarco_doc_00_28953614
    #     run_files = True   # msmarco_doc_00_28953614 is the document with 15109 mentions 
    
    # if docid == "msmarco_doc_00_28953614":
    print(f"docid is {docid}", flush=True)
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


filename = f"{datapath}timing/ed_coref_ndocs_{args.n_docs}_{args.search_corefs}"


with open(f"{filename}.pickle", "wb") as f:
    pickle.dump(measurements, f, protocol=pickle.HIGHEST_PROTOCOL)        


print("Done.")
