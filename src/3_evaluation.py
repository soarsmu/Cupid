from icecream import ic
import re
import json
from collections import OrderedDict


n_files = 5
def write_summary_to_file(output_file, summary):
    with open(output_file) as f:
        json.dump(summary, f)

def create_summary(alternative_recommendation_file = '', original_recommendation_file = '', top_n = 10):
    summary = {}

    # read alternative BR
    if alternative_recommendation_file != '':
        for i in range(n_files):
            # recommendation_file = f'''230323-spark-p1/recommend_ranknet_230423_spark_p1_v{i}_I-1'''
            with open(alternative_recommendation_file.format(i=i)) as f:
                lines = f.readlines()
                line_id = 1
                while line_id < len(lines):
                    if "Retrieving for" in lines[line_id]:
                        bug_id = re.search("report (.+?) \(Its", lines[line_id]).group(1)
                        master_id = re.search("Its master is (.+?)\)", lines[line_id]).group(1)
                        # ic(bug_id, master_id)

                        summary[bug_id] = summary.get(bug_id, {'master_id': master_id})
                        summary[bug_id]['recommendation'] = summary[bug_id].get('recommendation', {})

                        top_n_recommendations = lines[line_id+1:line_id+top_n+1]
                        for line in top_n_recommendations:
                            master_dup_id = re.search("\d+ - (.*?)\(real-sim-id", line).group(1).strip()
                            score = re.search(" \: (.*?) \+*?\n", line)
                            try:
                                score = score.group(1)
                            except:
                                ic(line)

                            summary[bug_id]['recommendation'][master_dup_id] = summary[bug_id]['recommendation'].get(master_dup_id, [])
                            summary[bug_id]['recommendation'][master_dup_id].append(score)

                        line_id = line_id+top_n+1
                        # ic(lines[line_id])
                    else:
                        line_id += 1

    # read original BR
    if original_recommendation_file != '':
        with open(original_recommendation_file) as f:
            lines = f.readlines()
            line_id = 1
            while line_id < len(lines):
                if "Retrieving for" in lines[line_id]:
                    bug_id = re.search("report (.+?) \(Its", lines[line_id]).group(1)
                    master_id = re.search("Its master is (.+?)\)", lines[line_id]).group(1)
                    # ic(bug_id, master_id)

                    summary[bug_id] = summary.get(bug_id, {'master_id': master_id})
                    summary[bug_id]['recommendation'] = summary[bug_id].get('recommendation', {})

                    top_n_recommendations = lines[line_id+1:line_id+top_n+1]
                    for line in top_n_recommendations:
                        master_dup_id = re.search("\d+ - (.*?)\(real-sim-id", line).group(1).strip()
                        score = re.search(" \: (.*?) \+*?\n", line)
                        try:
                            score = score.group(1)
                        except:
                            ic(line)

                        summary[bug_id]['recommendation'][master_dup_id] = summary[bug_id]['recommendation'].get(master_dup_id, [])
                        summary[bug_id]['recommendation'][master_dup_id].append(score)

                    line_id = line_id+top_n+1
                    # ic(lines[line_id])
                else:
                    line_id += 1
    # ic(summary)
    return summary

def create_summary_per_position(original_recommendation_file, alternative_recommendation_file, top_n = 10):
    summary = {}
    # read alternative BR
    for i in range(n_files):
        # recommendation_file = f'''230323-spark-p1/recommend_ranknet_230423_spark_p1_v{i}_I-1'''
        with open(alternative_recommendation_file.format(i=i)) as f:
            lines = f.readlines()
            line_id = 1
            while line_id < len(lines):
                if "Retrieving for" in lines[line_id]:
                    bug_id = re.search("report (.+?) \(Its", lines[line_id]).group(1)
                    master_id = re.search("Its master is (.+?)\)", lines[line_id]).group(1)

                    summary[bug_id] = summary.get(bug_id, {'master_id': master_id})
                    summary[bug_id]['recommendation'] = summary[bug_id].get('recommendation', {})

                    top_n_recommendations = lines[line_id+1:line_id+top_n+1]
                    
                    rank_counter = 1
                    for line in top_n_recommendations:
                        master_dup_id = re.search("\d+ - (.*?)\(real-sim-id", line).group(1)
                        score = re.search(" \: (.*?) \+*?\n", line)
                        try:
                            score = score.group(1)
                        except:
                            ic(line)

                        summary[bug_id]['recommendation'][master_dup_id] = summary[bug_id]['recommendation'].get(master_dup_id, {'rank': [], 'score': []})
                        summary[bug_id]['recommendation'][master_dup_id]['rank'].append(rank_counter)
                        summary[bug_id]['recommendation'][master_dup_id]['score'].append(score)

                        rank_counter += 1

                    line_id = line_id+top_n+1
                else:
                    line_id += 1

    # read original BR
    if original_recommendation_file != '':
        with open(original_recommendation_file) as f:
            lines = f.readlines()
            line_id = 1
            while line_id < len(lines):
                if "Retrieving for" in lines[line_id]:
                    bug_id = re.search("report (.+?) \(Its", lines[line_id]).group(1)
                    master_id = re.search("Its master is (.+?)\)", lines[line_id]).group(1)
                    # ic(bug_id, master_id)

                    summary[bug_id] = summary.get(bug_id, {'master_id': master_id})
                    summary[bug_id]['recommendation'] = summary[bug_id].get('recommendation', {})

                    top_n_recommendations = lines[line_id+1:line_id+top_n+1]
                    rank_counter = 1
                    for line in top_n_recommendations:
                        master_dup_id = re.search("\d+ - (.*?)\(real-sim-id", line).group(1)
                        score = re.search(" \: (.*?) \+*?\n", line)
                        try:
                            score = score.group(1)
                        except:
                            ic(line)

                        summary[bug_id]['recommendation'][master_dup_id] = summary[bug_id]['recommendation'].get(master_dup_id, {'rank': [], 'score': []})
                        summary[bug_id]['recommendation'][master_dup_id]['rank'].append(rank_counter)
                        summary[bug_id]['recommendation'][master_dup_id]['score'].append(score)

                        rank_counter += 1

                    line_id = line_id+top_n+1
                    # ic(lines[line_id])
                else:
                    line_id += 1

    # get summary per ranking
    for bug_id in summary:
        summary[bug_id]['ranking'] = summary[bug_id].get('ranking', {})
        for dup_id in summary[bug_id]['recommendation']:
            for r, score in zip(summary[bug_id]['recommendation'][dup_id]['rank'],
                                  summary[bug_id]['recommendation'][dup_id]['score']):
                summary[bug_id]['ranking'][r] = summary[bug_id]['ranking'].get(r, {})
                summary[bug_id]['ranking'][r][dup_id] = summary[bug_id]['ranking'][r].get(dup_id, [])
                summary[bug_id]['ranking'][r][dup_id].append(score)
                # summary[bug_id]['ranking'][r].append((dup_id, score))
    return summary

def agg_result(summary):
    temp_sum = {}
    for bug_id in summary:
        temp_sum[int(bug_id)] = summary[bug_id].copy()
        temp_sum[int(bug_id)]['max_score'] = {}
        temp_sum[int(bug_id)]['avg_score'] = {}
        temp_sum[int(bug_id)]['count'] = {}
        temp_sum[int(bug_id)]['sum_score'] = {}
        temp_sum[int(bug_id)]['avg_weighted_score'] = {}
        for master_dup_id in temp_sum[int(bug_id)]['recommendation']:
            temp_sum[int(bug_id)]['max_score'][int(master_dup_id)] = max([float(x) for x in summary[bug_id]['recommendation'][master_dup_id]])
            temp_sum[int(bug_id)]['avg_score'][int(master_dup_id)] = sum([float(x) for x in summary[bug_id]['recommendation'][master_dup_id]])/len(summary[bug_id]['recommendation'][master_dup_id])
            temp_sum[int(bug_id)]['sum_score'][int(master_dup_id)] = sum([float(x) for x in summary[bug_id]['recommendation'][master_dup_id]])
            temp_sum[int(bug_id)]['count'][int(master_dup_id)] = len(summary[bug_id]['recommendation'][master_dup_id])
            temp_sum[int(bug_id)]['avg_weighted_score'][int(master_dup_id)] = sum([float(x) for x in summary[bug_id]['recommendation'][master_dup_id]])/5     
    return temp_sum

def agg_result_per_position(summary, top_n=10):
    res = {}
    for bug_id in summary:
    # for bug_id in ['13336103']:
        res[bug_id] = {}
        res[bug_id]['master_id'] = summary[bug_id]['master_id']
        res[bug_id]['ranking'] = summary[bug_id]['ranking']

        # calculate max score
        for rank in range(top_n):
            # preprocess ranking
            temp = res[bug_id]['ranking'][rank+1].copy()
            for dup_id in temp:
                temp_scores = temp[dup_id]
                temp[dup_id] = {}
                temp[dup_id]['max'] = max([float(x.strip()) for x in temp_scores])
                temp[dup_id]['sum'] = sum([float(x.strip()) for x in temp_scores])
                temp[dup_id]['avg'] = sum([float(x.strip()) for x in temp_scores])/len(temp_scores)
                temp[dup_id]['count'] = len(temp_scores)

            # process max
            for type in ['max', 'sum', 'avg', 'count']:
                type_temp = {}
                for dup_id in temp:
                    type_temp[dup_id] = temp[dup_id][type]

                sorted_rank_by_score = dict(sorted(type_temp.items(), key=lambda x:x[1], reverse=True))
                # insert dup_id with highest score, and look for the next maximum score if it already exists
                for dup_id in sorted_rank_by_score:
                    if dup_id not in res[bug_id].get(type, []):
                        res[bug_id][type] = res[bug_id].get(type, [])
                        res[bug_id][type].append(dup_id)
                        break
    return res

def filter_result_per_score(agg_summary, top_n=10, score_fields=['max_score', 'avg_score', 'count', 'sum_score', 'avg_weighted_score'], per_position = False):
    temp_res = {}
    for bug_id in agg_summary:
        temp_res[bug_id] = {}
        temp_res[bug_id]['master_id'] = agg_summary[bug_id]['master_id']

        if not per_position:
            for score_type in score_fields:  
                # original_dict = dict(sorted(agg_summary[bug_id][score_type].items(), key = lambda x: x[1], reverse = True)[:top_n])
                
                ordered_dict = OrderedDict(sorted(agg_summary[bug_id][score_type].items(), key = lambda x: x[1], reverse = True)[:top_n])
                
                ordered_dict_1 = OrderedDict(sorted(agg_summary[bug_id][score_type].items(), key=lambda x: (-x[1], x[0]))[:top_n])
                
                # sorted_dict = {k: v for k, v in sorted(original_dict.items(), key=lambda item: item[1], reverse = True)}
                # if bug_id == 53959:
                    # ic(ordered_dict)
                temp_res[bug_id][score_type] = ordered_dict_1
        else:
            for score_type in score_fields:
                temp_res[bug_id][score_type] = agg_summary[bug_id][score_type][:top_n]
    
    # ic(temp_res[53959])
    return temp_res

def calculate_recall_rate(filtered_summary):
    res = {}
    for bug_id in filtered_summary:
        # if bug_id == 53959:
        #     ic(filtered_summary[bug_id])
            
        for key in filtered_summary[bug_id]:
            if key != 'master_id':
                res[key] = res.get(key, 0)
                if int(filtered_summary[bug_id]['master_id']) in [int(x) for x in filtered_summary[bug_id][key]]:
                    res[key] += 1
                    
    recall_rate = {}
    for key in res:
        recall_rate[key] = round(res[key]/len(filtered_summary), 3)
    return recall_rate

def calculate_recall_rate_at_k(agg_summary, k=10, score_fields =  ['max_score', 'avg_score', 'count', 'sum_score', 'avg_weighted_score'], per_position=False):
    filtered_summary = filter_result_per_score(agg_summary, top_n=k, score_fields = score_fields, per_position=per_position)
    recall_count = calculate_recall_rate(filtered_summary)
    return recall_count

if __name__ == '__main__':
    
    ## Spark
    # original_filepath = '../res/spark/recommend_ranknet_27_Aug_rep_sampled_spark_1_I-1'
    alternative_filepath = '../res/spark/cupid/recommend_ranknet_280423_spark_p5_flag_1-{i}_I-1'
    
    ### Spark prompt 1
    # alternative_filepath = '../res/spark/recommend_ranknet_24_Apr_rep_ChatGPT_p1_spark_v{i}_I-1'
    
    ### Spark prompt 2
    # alternative_filepath = '../res/spark/recommend_ranknet_24_Apr_rep_ChatGPT_p3_spark_v{i}_I-1'
    
    ### Spark no filtering
    # alternative_filepath = '../res/spark/no-filtering/recommend_ranknet_280423_spark_p5_v{i}_I-1'
    
    ### Spark filtering with length
    # alternative_filepath = '../res/spark/filtering_length/recommend_ranknet_280423_spark_length_{i}_I-1'
    
    ### Spark filtering with content
    # alternative_filepath = '../res/spark/filtering_content/recommend_ranknet_280423_spark_content_{i}_I-1'
    # Hadoop
    # original_filepath = '../res/hadoop/recommend_ranknet_27_Aug_rep_sampled_hadoop_1_I-1'
    # alternative_filepath = '../res/hadoop/recommend_ranknet_280423_hadoop_p5_flag_1-{i}_I-1'
    
    ## Kibana
    # original_filepath = '../res/kibana/recommend_ranknet_31_Aug_rep_kibana_1_I-1'
    # alternative_filepath = '../res/kibana/recommend_ranknet_280423_kibana_p5_flag_1-{i}_I-1'
    
    ## VSCode
    # original_filepath = '../res/vscode/recommend_ranknet_27_Aug_rep_sampled_vscode_1_I-1'
    # alternative_filepath = '../res/vscode/recommend_ranknet_280423_vscode_p5_flag_1-{i}_I-1'

    for n in range(10,11):
        ic("TOP_N, WITH ORIGINAL", n)
        recall_rate = {}

        # AGGREGATION TYPE 1 (GET TOP-N FIRST)
        # summary = create_summary(alternative_recommendation_file = alternative_filepath, original_recommendation_file = original_filepath, top_n=n)
        summary = create_summary(alternative_recommendation_file = alternative_filepath, original_recommendation_file = '', top_n=n)
        agg_summary = agg_result(summary)
        for k in range(10):
            recall_rate[k+1] = calculate_recall_rate_at_k(agg_summary, k=k+1)
        # recall_rate[10] = calculate_recall_rate_at_k(agg_summary, k=11)
        ic(recall_rate)
        
        for k in range(10):
            # ic(k+1, recall_rate[k+1]['sum_score'])
            print(recall_rate[k+1]['sum_score'])
        
        # AGGREGATION TYPE 2 (PER POSITION)
        # summary = create_summary_per_position(alternative_recommendation_file = alternative_filepath, original_recommendation_file = original_filepath, top_n=n)
        # agg_summary = agg_result_per_position(summary)
        # for k in range(10):
        #     recall_rate[k+1] = calculate_recall_rate_at_k(agg_summary, k=k+1, score_fields = ['max', 'count', 'sum', 'avg'], per_position=True)
        # ic(recall_rate)

        # ic("TOP_N, ONLY ORIGINAL", n)
        # summary = create_summary(original_recommendation_file = original_filepath, top_n=n)
        # agg_summary = agg_result(summary)
        # recall_rate = {}
        # for k in range(1):
        #     recall_rate[k+1] = calculate_recall_rate_at_k(agg_summary, k=k+1)
        # ic(recall_rate)
        # ic("---------------")

        # ic("TOP_N, ONLY ALTERNATIVES", n)
        # summary = create_summary(alternative_recommendation_file = alternative_filepath, top_n=n)
        # agg_summary = agg_result(summary)
        # recall_rate = {}
        # for k in range(1):
        #     recall_rate[k+1] = calculate_recall_rate_at_k(agg_summary, k=k+1)
        # ic(recall_rate)
        # ic("---------------")