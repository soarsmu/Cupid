"""
Extract test data from the original dataset
"""

import argparse
import pandas as pd
import json
import os
from tqdm import tqdm
from prompt_templates import prompt_tmps
from icecream import ic
import numpy as np
import re

data_folder = '../data/'
llm_data_folder = '../data/llm/'

def extract_text_from_test_data(project):
    """
    Extract original summary and description from the original dataset
    """
    
    with open(data_folder + 'raw/{}/test_{}.txt'.format(project, project), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    print(len(duplicate_bug_id))
    original_content_json = data_folder + 'raw/{}/{}.json'.format(project, project)
    with open(original_content_json, 'r') as f:
        original_content_lines = f.readlines()
    bug_ids, short_descs, descriptions = [], [], []
    for line in tqdm(original_content_lines):
        bug = json.loads(line)        
        if bug['bug_id'] in duplicate_bug_id:
            bug_ids.append(bug['bug_id'])
            short_descs.append(bug['short_desc'])
            descriptions.append(bug['description'])
    test_data = pd.DataFrame({'bug_id': bug_ids, 'short_desc': short_descs, 'description': descriptions})
    os.makedirs(llm_data_folder + project, exist_ok=True)
    test_data.to_csv(llm_data_folder + project + '/test_{}.csv'.format(project))

def investigate_data(project):
    desc_lens = []  
    with open(data_folder + 'raw/{}/test_{}.txt'.format(project, project), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    print(len(duplicate_bug_id))
    original_content_json = data_folder + 'raw/{}/{}.json'.format(project, project)
    with open(original_content_json, 'r') as f:
        original_content_lines = f.readlines()
    descriptions = []
    # long_count = 0
    for line in tqdm(original_content_lines):
        bug = json.loads(line)        
        if bug['bug_id'] in duplicate_bug_id:
            continue
        
        descriptions.append(bug['description'])
        # ic(bug['description'])
        # ic(bug['bug_id'], len(bug['description'].split()))
        desc_lens.append(len(bug['description'].split()))
    
    p25 = np.percentile(desc_lens, 25)
    p50 = np.percentile(desc_lens, 50)
    p75 = np.percentile(desc_lens, 75)
    ic(project)
    ic(p25, p50, p75)
    # ic(long_count)
    # Spark: ic| p25: 27.0, p50: 57.0, p75: 118.0
    # VSCode: ic| p25: 39.0, p50: 78.0, p75: 134.0
    # Hadoop: ic| p25: 24.0, p50: 47.0, p75: 93.0
    # Kibana: ic| p25: 40.0, p50: 74.0, p75: 134.0


def filter_length(project, length_threshold=118):
    """
    Ablation study 1: filter out the bug reports whose description 
    length is less than the threshold
    """
    
    df = pd.read_csv(llm_data_folder + project + '/test_{}.csv'.format(project), index_col=None)
    bug_ids = []
    run_flag = []
    for i, row in df.iterrows():
        bug_id = row['bug_id']
        bug_ids.append(bug_id)
        if len(str(row['description']).split()) < length_threshold:
            run_flag.append(0)
            continue
        run_flag.append(1)        
    df = pd.DataFrame({'bug_id': bug_ids, 'run_flag': run_flag})
    df.to_csv(llm_data_folder + project + '/ablation-filtering/test_{}_flag_length.csv'.format(project))

def filter_content(project):
    """
    Ablaion study 2: filter out the bug reports whose description does not contain
    URLs or code
    """
    df = pd.read_csv(llm_data_folder + project + '/test_{}.csv'.format(project), index_col=None)
    bug_ids = []
    run_flag = []
    pattern_1 = r"\w+\.\w+\.\w{1,}"
    pattern_2 = r"https?://\S+"
    
    for i, row in df.iterrows():
        bug_id = row['bug_id']
        bug_ids.append(bug_id)
        if re.search(pattern_1, str(row['description'])) or \
        re.search(pattern_2, str(row['description'])):
            run_flag.append(1)
            continue
        run_flag.append(0)
        
    df = pd.DataFrame({'bug_id': bug_ids, 'run_flag': run_flag})
    df.to_csv(llm_data_folder + project + '/ablation-filtering/test_{}_flag_content.csv'.format(project))
    
def filter_desc(project, length_threshold=134):
    """
    Final filtering we used.
    """
    
    df = pd.read_csv(llm_data_folder + project + '/test_{}.csv'.format(project), index_col=None)
    bug_ids = []
    run_flag = []
    pattern_1 = r"\w+\.\w+\.\w{1,}"
    pattern_2 = r"https?://\S+"
    
    for i, row in df.iterrows():
        bug_id = row['bug_id']
        bug_ids.append(bug_id)
        if len(str(row['description']).split()) >= length_threshold or \
        re.search(pattern_1, str(row['description'])) or \
        re.search(pattern_2, str(row['description'])):
            run_flag.append(1)
            continue
        run_flag.append(0)
        
    df = pd.DataFrame({'bug_id': bug_ids, 'run_flag': run_flag})
    df.to_csv(llm_data_folder + project + '/test_{}_run_flag_1.csv'.format(project))
    
    
def prepare_chatgpt_data(project):
    df = pd.read_csv(llm_data_folder + project + '/test_{}.csv'.format(project), index_col=None)
    bug_ids = []
    input_texts = []
    prompt_template = prompt_tmps[prompt]
    
    for i, row in df.iterrows():
        bug_id = row['bug_id']
        input_text = prompt_template.format(row['short_desc'], row['description'])
        bug_ids.append(bug_id)
        input_texts.append(input_text)
    df = pd.DataFrame({'bug_id': bug_ids, 'input_text': input_texts})
    df.to_csv(llm_data_folder + project + '/test_{}_prompt_{}.csv'.format(project, prompt))
    
def main():
    # extract_text_from_test_data(project)
    # prepare_chatgpt_data(project)
    # investigate_data(project)
    filter_length(project)
    # filter_content(project)
    # filter_desc(project)
    
if __name__ == '__main__':
    arguement_parser = argparse.ArgumentParser()
    arguement_parser.add_argument('--project', type=str, required=True, help='Project name')
    arguement_parser.add_argument('--prompt', type=str, required=True, help='Prompt variant')
    
    args = arguement_parser.parse_args()
    project = args.project
    prompt = args.prompt
    main()
    