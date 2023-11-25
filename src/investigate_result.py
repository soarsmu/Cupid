import re
from icecream import ic

def compare_two_files(res_1, res_2, TOP_N):
    res_1_hits = get_hits(res_1, TOP_N)
    res_2_hits = get_hits(res_2, TOP_N)
    
    # ic(len(res_1_hits), len(res_2_hits))
    # ic(res_2_hits | res_1_hits)
    # ic(res_1_hits | res_2_hits)
    # ic(set(res_1_hits.keys()) & set(res_2_hits.keys()))
    print('原先失败，现在成功的：')
    ic(len(set(res_1_hits.keys()) - set(res_2_hits.keys())))
    
    print('原先成功，现在失败的：')
    ic(set(res_2_hits.keys()) - set(res_1_hits.keys()))
    # ic(set(res_2_hits.keys()) - set(res_1_hits.keys()))
    print('------------------')
    
def get_hits(res_file, TOP_N):
    res_1_hits = {}
    with open(res_file) as f:
        lines = f.readlines()
        line_id = 1
        while line_id < len(lines):
            if "Retrieving for" in lines[line_id]:
                bug_id = re.search("report (.+?) \(Its", lines[line_id]).group(1)
                master_id = re.search("Its master is (.+?)\)", lines[line_id]).group(1)
                # ic(bug_id, master_id)
                
                top_n_recommendations = lines[line_id + 1:line_id + TOP_N + 1]
                for index, line in zip(range(TOP_N), top_n_recommendations):
                    if line.strip()[-1] == '+':
                        res_1_hits[bug_id] = index + 1
                        break
                line_id = line_id+TOP_N+1
            else:
                line_id += 1
    return res_1_hits

def get_all_hits():
    all_hits = set()
    for i in range(5):
        all_hits |= set(get_hits('../res/recommend_ranknet_260423_hadoop_p3_v{}_I-1'.format(i), 10).keys())
    ic(len(all_hits))
    # all_hits |= set(get_hits('../res/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1', 10).keys())
    # ic(len(all_hits))

def get_new_success():
    all_hits = set()
    for i in range(5):
        all_hits |= set(get_hits('../res/recommend_ranknet_24_Apr_rep_ChatGPT_p1_spark_v{}_I-1'.format(i), 10).keys())
        
    new_success = all_hits -  set(get_hits('../res/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1', 10).keys())
    ic(new_success)
    
if __name__ == '__main__':
    # for i in range(5):
    #     compare_two_files('../res/hadoop/recommend_ranknet_260423_hadoop_p3_v{}_flag_I-1'.format(i), 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)
    # ic("P4 without flag")
    # compare_two_files('../res/hadoop/recommend_ranknet_270423_hadoop_p4_I-1', 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)
    
    # ic("P4 with flag")
    # compare_two_files('../res/hadoop/recommend_ranknet_270423_hadoop_p4_flag_I-1', 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)
    
    # ic("P4 with flag 1")
    # compare_two_files('../res/hadoop/recommend_ranknet_270423_hadoop_p4_flag_1_I-1', 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)
    
    # ic("P3 without flag")
    # compare_two_files('../res/hadoop/recommend_ranknet_260423_hadoop_p3_v0_I-1', 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)

    # ic("P3 with flag")
    # compare_two_files('../res/hadoop/recommend_ranknet_260423_hadoop_p3_v0_flag_I-1', 
    #                   '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1', 10)
    
    # ic("P4 with flag")
    # compare_two_files('../res/spark/recommend_ranknet_270423_spark_p4_flag_I-1', 
    #                   '../res/spark/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1', 10)
    
    project = 'vscode'
    ic(project)
    ic("P5 with flag 1")
    compare_two_files('../res/{}/recommend_ranknet_280423_{}_p5_flag_1_I-1'.format(project, project), 
                      '../res/{}/recommend_ranknet_27_Aug_rep_sampled_{}_1_I-1'.format(project, project), 10)
    
    # ic("P3 with flag")
    # compare_two_files('../res/spark/recommend_ranknet_270423_spark_p3_v0_flag_I-1', 
    #                   '../res/spark/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1', 10)
    
    
    # get_all_hits()
    # get_hits('../res/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1', 10)
    # get_new_success()