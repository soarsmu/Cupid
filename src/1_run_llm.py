from transformers import AutoTokenizer
import transformers
import torch
import pandas as pd
import os
import time
import logging
import json
from tqdm import tqdm
import argparse

model_dict = {
    'vicuna': 'lmsys/vicuna-13b-v1.5',
    'wizardlm': 'WizardLM/WizardLM-13B-V1.2',
    'llama2': "meta-llama/Llama-2-13b-chat-hf"
}

datasets = ['hadoop', 'kibana', 'spark']
prompt_folder = '../prompt/'
result_folder = '../results/'

def generate(prompt_template, test_csv, prompt_variant, run_id):
    df = pd.read_csv(test_csv)
    short_desc_list = df['short_desc'].tolist()
    desc_list = df['description'].tolist()
    bug_id_list = df['bug_id'].tolist()
    cur_result_folder = result_folder + '{}/{}/{}/{}'.format(model_name, dataset_name, prompt_variant, run_id)
    os.makedirs(cur_result_folder, exist_ok=True)
        
    for i in tqdm(range(len(short_desc_list))):
        if os.path.exists(os.path.join(cur_result_folder, '{}.txt'.format(bug_id_list[i]))):
            continue
        
        prompt = prompt_template.format(short_desc_list[i], desc_list[i])
        logging.info('The template for bug report is: {}'.format(prompt))
        tokenizer = AutoTokenizer.from_pretrained(model_dict[model_name])
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_dict[model_name],
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto"
        )
        
        start = time.time()
        sequences = pipeline(
            prompt,
            max_length=2048,
            # do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
        
        logging.info('time taken: {}'.format(time.time() - start))
        result_file = os.path.join(cur_result_folder, '{}.txt'.format(bug_id_list[i]))    
        with open(result_file, 'w') as f:
            for seq in sequences:
                # logging.info(seq['generated_text'])
                f.write(seq['generated_text'] + '\n')

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--dataset', '-d', type=str, required=True)
    args.add_argument('--model', '-m', type=str, required=True)
    args.add_argument('--prompt', '-p', type=str, required=True)
    args.add_argument('--run_id', '-r', type=int, required=True)
    args = args.parse_args()
    
    with open('../prompt/prompt_template.json', 'r') as f:
        prompt_tmps = json.load(f)
        
    prompt_variant = args.prompt
    model_name = args.model
    dataset_name = args.dataset
    prompt_template = prompt_tmps[prompt_variant]
    run_id = args.run_id
    
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s %(message)s', 
        handlers=[
            logging.FileHandler("../log/{}_{}_{}_{}.log".format(dataset_name, model_name, prompt_variant, run_id)),
            logging.StreamHandler()
        ]
    )
    test_csv = '../data/llm/{}/test_{}.csv'.format(dataset_name, dataset_name)
    generate(prompt_template, test_csv, prompt_variant, run_id)