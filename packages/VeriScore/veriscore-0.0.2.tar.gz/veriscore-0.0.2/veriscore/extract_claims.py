"""
This script is written to extract claims from the model responses.
model generations: /data/yixiao/atomic_claims/data/model_generation_decomposition/model_generations
"""

import os
import pdb
import json
import argparse
from tqdm import tqdm
from .ClaimExtractor import ClaimExtractor
#
# args = argparse.ArgumentParser()
# args.add_argument("--input_file", type=str, required=True)
# args = args.parse_args()
#
# input_file_names = ['Mistral-7B-Instruct-v0.1',
#                     'Mistral-7B-Instruct-v0.2',
#                     'Mixtral-8x7B-Instruct-v0.1',
#                     'Mixtral-8x22B-Instruct-v0.1',
#                     'gpt-4-0125-preview',
#                     'gpt-3.5-turbo-1106',
#                     'gpt-3.5-turbo-0613',
#                     'claude-3-opus-20240229',
#                     'claude-3-sonnet-20240229',
#                     'claude-3-haiku-20240307',
#                     'dbrx-instruct',
#                     'OLMo-7B-Instruct', ]
#
# abstain_responses = ["I'm sorry, I cannot fulfill that request.",
#                      "I'm sorry, I can't fulfill that request.",
#                      "I'm sorry, but I cannot fulfill that request.",
#                      "I'm sorry, but I can't fulfill that request.",
#                      "Sorry, but I can't fulfill that request.",
#                      "Sorry, I can't do that."]
#
# # read data
# input_file_name = args.input_file
# assert input_file_name in input_file_names
# input_file_dir = f"data/model_generation_decomposition/model_generations/data_{input_file_name}.jsonl"
# with open(input_file_dir, "r") as f:
#     data = [json.loads(x) for x in f.readlines() if x.strip()]
#
# # initialize objects
# model_name = "gpt-4-0125-preview"
# claim_extractor = ClaimExtractor(model_name, input_file_name)
#
# output_dir = f"data/model_generation_decomposition/decomposed_responses/claims_{input_file_name}.jsonl"
# with open(output_dir, "a+") as f:
#     for dict_item in tqdm(data[1558:]):
#         # get necessary info
#         question = dict_item["question"]
#         response = dict_item["response"]
#         prompt_source = dict_item["prompt_source"]
#         model = dict_item["model"]
#
#         # skip abstained responses
#         if response.strip() in abstain_responses:
#             output_dict = {"question": question.strip(),
#                            "response": response.strip(),
#                            "abstained": True,
#                            "prompt_source": prompt_source,
#                            "model": model,}
#             f.write(json.dumps(output_dict) + "\n")
#             continue
#
#         # extract claims
#         snippet_lst, fact_lst_lst, all_facts_lst, prompt_tok_cnt, response_tok_cnt = claim_extractor.qa_scanner_extractor(question, response)
#
#         # write output
#         output_dict = {"question": question.strip(),
#                        "response": response.strip(),
#                        "abstained": False, # "abstained": False, "abstained": True
#                        "snippet_lst": snippet_lst,
#                        "fact_lst_lst": fact_lst_lst,
#                        "all_facts_lst": all_facts_lst,
#                        "prompt_tok_cnt": prompt_tok_cnt,
#                        "response_tok_cnt": response_tok_cnt,
#                        "prompt_source": prompt_source,
#                        "model": model,}
#         f.write(json.dumps(output_dict) + "\n")

input_file_names = ['Mistral-7B-Instruct-v0.1',
                    'Mistral-7B-Instruct-v0.2',
                    'Mixtral-8x7B-Instruct-v0.1',
                    'Mixtral-8x22B-Instruct-v0.1',
                    'gpt-4-0125-preview',
                    'gpt-3.5-turbo-1106',
                    'gpt-3.5-turbo-0613',
                    'claude-3-opus-20240229',
                    'claude-3-sonnet-20240229',
                    'claude-3-haiku-20240307',
                    'dbrx-instruct',
                    'OLMo-7B-Instruct', ]

abstain_responses = ["I'm sorry, I cannot fulfill that request.",
                     "I'm sorry, I can't fulfill that request.",
                     "I'm sorry, but I cannot fulfill that request.",
                     "I'm sorry, but I can't fulfill that request.",
                     "Sorry, but I can't fulfill that request.",
                     "Sorry, I can't do that."]

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--data_dir", type=str, default='data')
    args.add_argument("--input_file", type=str, required=True)
    args.add_argument("--output_dir", type=str, default='data')
    args.add_argument("--cache_dir", type=str, default='data/cache')
    args.add_argument("--model_name", type=str, default="gpt-4-0125-preview")
    args = args.parse_args()

    input_file_name = "".join(args.input_file.split('.')[:-1])
    # assert input_file_name in input_file_names

    input_path = os.path.join(args.data_dir, args.input_file)
    with open(input_path, "r") as f:
        data = [json.loads(x) for x in f.readlines() if x.strip()]

    # initialize objects
    model_name = args.model_name
    claim_extractor = ClaimExtractor(model_name, input_file_name, args.cache_dir)

    output_dir = args.output_dir
    output_file = f"claims_{input_file_name}.jsonl"
    output_path = os.path.join(output_dir, output_file)

    print(os.path.abspath(output_path))

    with open(output_path, "a+") as f:

        for dict_item in tqdm(data):
            # get necessary info
            question = dict_item["question"]
            response = dict_item["response"]
            prompt_source = dict_item["prompt_source"]
            model = dict_item["model"]

            # skip abstained responses
            if response.strip() in abstain_responses:
                output_dict = {"question": question.strip(),
                               "response": response.strip(),
                               "abstained": True,
                               "prompt_source": prompt_source,
                               "model": model,}
                f.write(json.dumps(output_dict) + "\n")
                continue

            # extract claims
            snippet_lst, claim_lst_lst, all_claim_lst, prompt_tok_cnt, response_tok_cnt = claim_extractor.qa_scanner_extractor(question, response)

            # write output
            output_dict = {"question": question.strip(),
                           "prompt_source": prompt_source,
                           "response": response.strip(),
                           "prompt_tok_cnt": prompt_tok_cnt,
                           "response_tok_cnt": response_tok_cnt,
                           "model": model,
                           "abstained": False, # "abstained": False, "abstained": True
                           "claim_lst_lst": claim_lst_lst,
                           "all_claim_lst": all_claim_lst
                           }
            f.write(json.dumps(output_dict) + "\n")