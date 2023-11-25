import logging
import pandas as pd
from icecream import ic

def get_logger(log_path):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    print('Logging to {}'.format(log_path))
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s', datefmt = '%F %A %T'))
    logger.addHandler(file_handler)

    # Logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(stream_handler)
    
    return logger

def read_need_run_ids(flag_file):
    flag_df = pd.read_csv(flag_file)
    need_run = set()
    for index, row in flag_df.iterrows():
        if row['run_flag'] == 1:
            need_run.add(str(row['bug_id'])) # <str>
    ic(len(need_run))
    return need_run