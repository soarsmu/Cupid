import argparse
import pandas as pd
import re
from tqdm import tqdm
import ujson
from icecream import ic
from utils import read_need_run_ids
import sys

data_folder = '../data/'
llm_data_folder = '../data/llm/'
result_folder = '../results/'

def extract_text_generated_by_llm(original_csv, to_save_csv, flag_file):
    """
    Ablation study 1: (1) filtering length (2) filtering content
    """
    
    ic(flag_file)
    
    original_df = pd.read_csv(original_csv)
    bug_ids = []
    summaries, descriptions = [], []
    
    need_run = read_need_run_ids(flag_file)
    not_count = 0
    for i, row in original_df.iterrows():
        bug_id = row['bug_id']        
        
        if not str(bug_id) in need_run:
            not_count += 1
            continue
        
        with open(llm_data_folder + dataset + '/prompt-{}-{}/{}.txt'.format(prompt, times, bug_id), 'r') as f:
            lines = f.readlines()
        
        rephrased_summary, rephrased_description = '', ''
        for line in lines:            
            summary_match = re.match(r'^\d*\.?\s*Summary(?:\s+\d+)?:\s+(.+)', line.strip())
            
            if summary_match:
                rephrased_summary = summary_match.group(1)
                summaries.append(rephrased_summary)
            
            if len(rephrased_summary) > 0:
                description_match = re.match(r'^\d*\.?\s*Description(?:\s+\d+)?:\s+(.+)', line.strip())
                if description_match:
                    rephrased_description = description_match.group(1)
                    descriptions.append(rephrased_description)
                    bug_ids.append(bug_id)
                    rephrased_summary = ''
                    rephrased_description = ''
                    
    bug_dict = dict()
    for bug in bug_ids:
        bug_dict[bug] = bug_dict.get(bug, 0) + 1
    for bug in bug_dict:
        if bug_dict[bug] == 2:
            print(bug)
    ic(not_count)
    
    ic(len(bug_ids), len(summaries), len(descriptions))
    
    pd.DataFrame({
        'bug_id': bug_ids, 
        'summary': summaries, 
        'description': descriptions
    }).to_csv(to_save_csv)


def extract_text_generated_by_llm_all(to_save_csv):
    """
    Ablation study 1: (3) no filtering
    """
    
    original_csv = llm_data_folder + dataset + '/test_{}.csv'.format(dataset)
    original_df = pd.read_csv(original_csv)
    bug_ids = []
    all_bug_ids = set(original_df['bug_id'].tolist())
    summaries, descriptions = [], []
    prompt_result_folder = result_folder + '{}/{}/{}/{}/'.format(model, dataset, prompt, times)
    
    # Regular expression pattern to match keywords
    pattern_summary = r"ASSISTANT: Summary Keywords: (.*?)$"
    extact_pattern_summary = "ASSISTANT: Summary Keywords:"
    
    pattern_description = r"Description Keywords: (.*)"

    for i, row in original_df.iterrows():
        bug_id = row['bug_id']
        summary_style_1 = 0
        
        with open(prompt_result_folder + "{}.txt".format(bug_id), 'r') as f:
            lines = f.readlines()
        
        rephrased_summary, rephrased_description = '', ''
        seen_description = False
        summary_keywords, description_keywords = [], []
        
        for line in lines:
            line = line.strip()
            summary_match = re.match(pattern_summary, line)
            if summary_match:
                summary_style_1 = 1
                rephrased_summary = summary_match.group(1).strip()                
            elif summary_style_1 != 1 and line == extact_pattern_summary:
                summary_style_1 = 2
            elif summary_style_1 == 2 and not seen_description:                
                summary_keywords.append(line.strip('* ').strip())
                
            if summary_style_1 == 1:
                description_match = re.match(pattern_description, line)
                if description_match:
                    rephrased_description = description_match.group(1).strip()
                    descriptions.append(rephrased_description)
                    if len(rephrased_summary) > 0:
                        summaries.append(rephrased_summary)
                    bug_ids.append(bug_id)
            elif summary_style_1 == 2 and line == 'Description Keywords:':
                seen_description = True
            elif summary_style_1 == 2 and seen_description:
                description_keywords.append(line.strip('* ').strip())
        
            
        if len(description_keywords) > 0:
            summaries.append(' '.join(summary_keywords))
            descriptions.append(' '.join(description_keywords))
            bug_ids.append(bug_id)
    missed_bug_ids = all_bug_ids - set(bug_ids)
    ic(len(missed_bug_ids))
    ic(missed_bug_ids)
    
    bug_dict = dict()
    for bug in bug_ids:
        bug_dict[bug] = bug_dict.get(bug, 0) + 1
    for bug in bug_dict:
        if bug_dict[bug] == 2:
            print(bug)
    
    ic(len(bug_ids), len(summaries), len(descriptions))
    
    pd.DataFrame({
        'bug_id': bug_ids, 
        'summary': summaries, 
        'description': descriptions
    }).to_csv(to_save_csv)
    
    
def seperate_five_versions():
    """
    Seperate the rephrased bug reports into five versions, 
    each version contains the rephrased bug reports for each bug.
    """
    
    rephrased_file = llm_data_folder + dataset + '/test_{}_prompt_{}_rephrased.csv'.format(dataset, prompt)
    df = pd.read_csv(rephrased_file)
    bug_text = dict()
    bug_seen_times = dict()
    five_versions = {0: [], 1: [], 2: [], 3: [], 4: []}
    
    for i, row in df.iterrows():
        bug_id = row['bug_id']
        summary = row['summary']
        description = row['description']
        seen_times = bug_seen_times.get(bug_id, 0)
        five_versions[seen_times].append((bug_id, summary, description))
        bug_seen_times[bug_id] = seen_times + 1
    
    for i in range(5):
        df = pd.DataFrame(five_versions[i], columns=['bug_id', 'summary', 'description'])
        df.to_csv(llm_data_folder + dataset + '/test_{}_prompt_{}_rephrased_{}.csv'.format(dataset, prompt, i))
        
        
def write_back_json_five():
    with open(data_folder + 'raw/{}/test_{}.txt'.format(dataset, dataset), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    ic(len(duplicate_bug_id))
    
    original_content_json = data_folder + 'raw/{}/{}.json'.format(dataset, dataset)
    
    for i in range(5):
        df = pd.read_csv(llm_data_folder + dataset + '/test_{}_prompt_{}_rephrased_{}.csv'.format(dataset, prompt, i))
        
        with open(original_content_json, 'r') as f:
            original_content_lines = f.readlines()
        
        output_lines = []
        for line in tqdm(original_content_lines):
            bug = ujson.loads(line)
              
            if bug['bug_id'] in duplicate_bug_id:
                try:
                    row = df[df['bug_id'] == int(bug['bug_id'])].iloc[0]
                except IndexError:
                    print(type(bug['bug_id']))
                    print(bug['bug_id'])
                bug['short_desc'] = row['summary']
                bug['description'] = row['description']
            
            output_lines.append(ujson.dumps(bug))
            
        with open(llm_data_folder + '{}/{}_p{}_v{}.json'.format(dataset, dataset, prompt, i), 'w') as f:
            for bug in output_lines:
                f.write(bug)
                f.write('\n')

def write_back_json_single(df_file):
    with open(data_folder + 'raw/{}/test_{}.txt'.format(dataset, dataset), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    ic(len(duplicate_bug_id))
    
    original_content_json = data_folder + 'raw/{}/{}.json'.format(dataset, dataset)
    
    df = pd.read_csv(df_file)
    
    with open(original_content_json, 'r') as f:
        original_content_lines = f.readlines()        
    
    output_lines = []
    for line in tqdm(original_content_lines):
        bug = ujson.loads(line)        
        if bug['bug_id'] in duplicate_bug_id:
            try:
                row = df[df['bug_id'] == int(bug['bug_id'])].iloc[0]
            except IndexError:
                print(type(bug['bug_id']))
                print(bug['bug_id'])
            bug['short_desc'] = row['summary']
            bug['description'] = row['description']
        
        output_lines.append(ujson.dumps(bug))
        
    with open(llm_data_folder + '{}/{}_p{}_v{}.json'.format(dataset, dataset, prompt, times), 'w') as f:
        for bug in output_lines:
            f.write(bug)
            f.write('\n')

def write_back_json_single_with_flags(df_file, flag_file, target_file):
    with open(data_folder + 'raw/{}/test_{}.txt'.format(dataset, dataset), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    ic(len(duplicate_bug_id))
    
    need_run = read_need_run_ids(flag_file)
    
    original_content_json = data_folder + 'raw/{}/{}.json'.format(dataset, dataset)
    
    df = pd.read_csv(df_file)
    
    with open(original_content_json, 'r') as f:
        original_content_lines = f.readlines()
    
    output_lines = []
    for line in tqdm(original_content_lines):
        bug = ujson.loads(line)

        if bug['bug_id'] in duplicate_bug_id and bug['bug_id'] in need_run:
            try:
                row = df[df['bug_id'] == int(bug['bug_id'])].iloc[0]
            except IndexError:
                print(type(bug['bug_id']))
                print(bug['bug_id'])
                
            bug['short_desc'] = row['summary']
            bug['description'] = row['description']
        
        output_lines.append(ujson.dumps(bug))
        
    with open(target_file, 'w') as f:
        for bug in output_lines:
            f.write(bug)
            f.write('\n')

def write_back_json_with_flags(flag_file):
    with open(data_folder + 'raw/{}/test_{}.txt'.format(dataset, dataset), 'r') as f:
        test_data = f.readlines()
    duplicate_bug_id = set()
    for bug_id in test_data[2].split():
        duplicate_bug_id.add(bug_id)
    ic(len(duplicate_bug_id))
    
    flag_df = pd.read_csv(flag_file)
    need_run = set()
    for index, row in flag_df.iterrows():
        if row['run_flag'] == 1:
            need_run.add(str(row['bug_id']))
    ic(len(need_run))
    
    original_content_json = data_folder + 'raw/{}/{}.json'.format(dataset, dataset)
    
    for i in range(5):
        df = pd.read_csv(llm_data_folder + dataset + '/test_{}_prompt_{}_rephrased_{}.csv'.format(dataset, prompt, i))
        
        with open(original_content_json, 'r') as f:
            original_content_lines = f.readlines()
        
        output_lines = []
        for line in tqdm(original_content_lines):
            bug = ujson.loads(line)        
            if bug['bug_id'] in duplicate_bug_id and bug['bug_id'] in need_run:
                try:
                    row = df[df['bug_id'] == int(bug['bug_id'])].iloc[0]
                except IndexError:
                    print(type(bug['bug_id']))
                    print(bug['bug_id'])
                bug['short_desc'] = row['summary']
                bug['description'] = row['description']
            
            output_lines.append(ujson.dumps(bug))
            
        with open(llm_data_folder + '{}/{}_p{}_v{}_flag.json'.format(dataset, dataset, prompt, i), 'w') as f:
            for bug in output_lines:
                f.write(bug)
                f.write('\n')
                
def main():
    extract_text_generated_by_llm_all(llm_data_folder + dataset + '/test_{}_prompt_{}_all-{}_rephrased.csv'.format(dataset, prompt, times))
    
    # extract_text_generated_by_chatgpt(llm_data_folder + dataset + '/test_{}_p{}_v{}_length_rephrased.csv'.format(dataset, prompt, times))
    
    # extract_text_generated_by_chatgpt_no_filtering(llm_data_folder + dataset + '/test_{}_prompt_{}_all-{}_rephrased.csv'.format(dataset, prompt, times))
    
    # save_one_version()
    # seperate_five_versions()
    # write_back_json_single(llm_data_folder + dataset + '/test_{}_prompt_{}_all-{}_rephrased.csv'.format(dataset, prompt, times))
    
    ### Ablation study - w/ length only
    # target_file = llm_data_folder + '{}/ablation-filtering/{}_p{}_length-{}.json'.format(dataset, dataset, prompt, times)
    # flag_file = llm_data_folder + '{}/ablation-filtering/test_{}_flag_length.csv'.format(dataset, dataset)
    
    ### Ablation study - w/ content only
    # target_file = llm_data_folder + '{}/ablation-filtering/{}_p{}_content-{}.json'.format(dataset, dataset, prompt, times)
    # flag_file = llm_data_folder + '{}/ablation-filtering/test_{}_flag_content.csv'.format(dataset, dataset)
    
    ### Ablation study - all
    # flag_file = llm_data_folder + '{}/test_{}_run_flag_1.csv'.format(dataset, dataset)
    # rephrased_file = llm_data_folder + dataset + '/test_{}_prompt_{}_all-{}_rephrased.csv'.format(dataset, prompt, times)
    
    # write_back_json_single_with_flags(rephrased_file, flag_file=flag_file, target_file=target_file)

    # write_back_json_with_flags()
    
if __name__ == '__main__':
    arguement_parser = argparse.ArgumentParser()
    arguement_parser.add_argument('--dataset', '-d', type=str, required=True)
    arguement_parser.add_argument('--model', '-m', type=str, required=True)
    arguement_parser.add_argument('--prompt', '-p', type=str, required=True, help='Prompt variant')
    arguement_parser.add_argument('--run', '-r', type=int, required=True, help='Run times')
    args = arguement_parser.parse_args()
    dataset = args.dataset
    model = args.model
    prompt = args.prompt
    times = args.run
    main()