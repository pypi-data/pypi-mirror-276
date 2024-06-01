import os
import pdb
import json
import random
import argparse
from tqdm import tqdm
from SearchAPI import SearchAPI

# add argparse argument
parser = argparse.ArgumentParser()
parser.add_argument("--multiple", type=str, default="5")
args = parser.parse_args()

"""
Read in extracted claim file
"""
begin = 400 * (int(args.multiple) - 1)
end = 400 * int(args.multiple)

file_dir = f"fine_tune_code_data/data/run_ft-ed_models_on_110_datapoints/4800_response_claim_extracted/merged_sampled_data_4800_extracted_{begin}_{end}.jsonl"

"""
Get search results for each claim
Store as a dictionary {claim: {"search_results": [search_results]}}
"""
# initialize search api
fetch_search = SearchAPI()

# read in extracted claim data
with open(file_dir, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

# set up output directory
out_dir = f"fine_tune_code_data/data/run_ft-ed_models_on_110_datapoints/4800_response_claim_extracted_w_evidence/merged_sampled_data_4800_extracted_{begin}_{end}_searched.jsonl"
os.makedirs(os.path.dirname(out_dir), exist_ok=True)

# get the pick up point
try:
    with open(out_dir, "r") as f:
        pick_up_point = len(f.readlines())
        print(f"Pick up point: {pick_up_point}")
except:
    pick_up_point = 0
    print("No pick up point")
    pass

# iterate through each data point and get search results
print(f"Begin{begin} End{end} Multiple {args.multiple}")
with open(out_dir, "a+") as f:
    for dict_item in tqdm(data[pick_up_point:]):
        if dict_item['abstained'] == True:
            f.write(json.dumps(dict_item) + "\n")
            continue
        
        claim_lst = dict_item["all_claim_lst"]
        if claim_lst == ["No verifiable claim."]:
            dict_item["claim_srch_res_lst"] = []
            f.write(json.dumps(dict_item) + "\n")
            continue
        claim_snippets = fetch_search.get_snippets(claim_lst)
        dict_item["claim_srch_res_lst"] = claim_snippets

        f.write(json.dumps(dict_item) + "\n")
        f.flush()
