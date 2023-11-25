import pandas as pd
from tqdm import tqdm
import time, os
from utils import get_logger
import argparse
from revChatGPT.V1 import Chatbot
from revChatGPT.typings import Error
from icecream import ic

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJzb2Fyc211Y2hhdGdwdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1TcWtxS1FpSDllQmE3MWg2S3RvVmhXTlYifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDYzZmVlNWQ4YTBmYzhhMTkyYzk5YmNhZiIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODI5Nzk3MDAsImV4cCI6MTY4NDE4OTMwMCwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvZmZsaW5lX2FjY2VzcyJ9.HPZkxF9U7nav3e81Qo-7qEoxnR-T0gVrvdIpeXdV5tvCoveKyIbAeSo888okMFxaUyvwk-I3IF4cZjVo4oU6HMEiHARawtziH1VFn6tpB3N5QSay5NYkmifpNVqFEz0PqCX-tTQS1f2MAVIknMOLxhcP74zpDcYZdrUZYEjFdVqeQNWguVDiaAAEH8I3WgEZVwjXr7atyl2yCN2S9fRwdMLhC0vFyYawfpzRLEmdq-Ew_CojbKLF36DLUuFbGJygyFQoeQLJOJW2T-qVIFkhyluQwQxqbeKkgWqd2nazPDKw96QhrYqwKBvULrqWxxOI2a_P-szQHRNlrwObjhnXOQ"

# access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ6aGFvemhlbmdjY0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci15MzR4aTI1MU1MbVRxSkNvVTFjQllmQ0cifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1MjE3MDMyODQ4NzQ4ODg2MDE2IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4MjEzODI3MCwiZXhwIjoxNjgzMzQ3ODcwLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.Ul9qF9dvNXCJUa5htTbJ2fawKsx0yO-WQpVwR7xKzQsIPA2ydrhhy9fUFPIy560Fil1J6OJ7IVJa-5jbo5yTAoTpVotbr3u2tRC-LeY3SBfffOR7P1QfBclGSG-aKKRw7Ve6ah-pOSpxwP8nsab3S6ipP6onOHSTgWKsXRDUApf_sYkZLuqGqWBqQh71Rw3oF4iUjY5CtvF_p_wJtyVRJjs00KBx4zxcOSba5r85F4c6je5XPq5fVW-BobBERNo-Bvo3T9BxeROnTyvSaZFhNp-DH7DEOM97cIsGpiTovmGpQYhkNnXBB0hDcoForyILDk92awl6WNZEnOcUepaDBA"


def init_chat():
    return Chatbot(config={"access_token": access_token})

def revise(test_csv, logger, res_folder):
    os.makedirs(res_folder, exist_ok=True)
    
    df = pd.read_csv(test_csv)
    
    flag_csv = data_folder + 'chatgpt/{}/test_{}_run_flag_1.csv'.format(project, project)
    flag_df = pd.read_csv(flag_csv)
    need_run = set()
    for index, row in flag_df.iterrows():
        if row['run_flag'] == 1:
            need_run.add(row['bug_id'])
    ic(len(need_run))
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        bug_id = row['bug_id']
        prompt = str(row["input_text"])
        
        if not bug_id in need_run:
            # ic('Skip bug_id: {}'.format(bug_id))
            continue
        
        if os.path.exists(res_folder + '{}.txt'.format(bug_id)):
            continue
        
        time.sleep(10)
        # logger.info('Sleep for 20 seconds')
            
        response = ''
        chatbot = init_chat()
        try:
            for data in chatbot.ask(prompt):
                response = data["message"]
        # except requests.exceptions.HTTPError as e:
        #     logger.info('HTTPError: {}'.format(e))
        #     logger.info('Error for Bug Report #{}: '.format(bug_id))
        #     continue
        except Error as e:
            logger.info('HTTPError: {}'.format(e))
            logger.info('Error for Bug Report #{}: '.format(bug_id))
            continue
        with open(res_folder + '{}.txt'.format(bug_id), 'w') as f:
            f.write('{}'.format(response))
        logger.info('Response for Bug Report #{}: {}'.format(bug_id, response))

def revise_no_filtering(test_csv, logger, res_folder):
    os.makedirs(res_folder, exist_ok=True)
    
    df = pd.read_csv(test_csv)
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        bug_id = row['bug_id']
        prompt = str(row["input_text"])
        
        if os.path.exists(res_folder + '{}.txt'.format(bug_id)):
            continue
        
        time.sleep(10)
            
        response = ''
        chatbot = init_chat()
        try:
            for data in chatbot.ask(prompt):
                response = data["message"]
        # except requests.exceptions.HTTPError as e:
        #     logger.info('HTTPError: {}'.format(e))
        #     logger.info('Error for Bug Report #{}: '.format(bug_id))
        #     continue
        except Error as e:
            logger.info('HTTPError: {}'.format(e))
            logger.info('Error for Bug Report #{}: '.format(bug_id))
            continue
        with open(res_folder + '{}.txt'.format(bug_id), 'w') as f:
            f.write('{}'.format(response))
        logger.info('Response for Bug Report #{}: {}'.format(bug_id, response))

if __name__ == '__main__':
    arguement_parser = argparse.ArgumentParser(description='Process an integer.')
    arguement_parser.add_argument('--project', type=str, required=True, help='Project name')
    arguement_parser.add_argument('--prompt', type=str, required=True, help='Prompt variant')
    arguement_parser.add_argument('--times', type=str, required=True, help='Repeated times')
    
    args = arguement_parser.parse_args()
    project = args.project
    prompt = args.prompt
    times = args.times
    
    data_folder = '../data/'
    chatgpt_data_folder = '../data/chatgpt/'
    
    logger = get_logger('../log/run-{}-prompt-{}-{}.log'.format(project, prompt, times))
    # revise(chatgpt_data_folder + '{}/test_{}_prompt_{}.csv'.format(project, project, prompt), 
        # logger, chatgpt_data_folder + '{}/prompt-{}-{}/'.format(project, prompt, times))
    revise_no_filtering(chatgpt_data_folder + '{}/test_{}_prompt_{}.csv'.format(project, project, prompt), 
        logger, chatgpt_data_folder + '{}/prompt-{}-{}/'.format(project, prompt, times))