# Data
Please download the data from this [Google Drive](https://drive.google.com/file/d/1Wc4dtiGZHxhTkyKYE20Jte6zhad4_n43/view?usp=share_link).
Please decompress the data (`public_data.tar.gz`) and you will get the following structure:

```bash
Three sub-folders:
+ ChatGPT: response and the updated bug repository information
    - Spark
    - Hadoop
    - Kibana
+ Raw: training-split, validation, training bug report pairs
    useful for runing REP, SABD, and Siamese Pair
    - Spark
    - Hadoop
    - Kibana
+ REP: the dbrd_test.txt are used by REP
    - Spark
        + final Cupid: dbrd_test_p5_flag_1-*.txt
        + prompt 1: dbrd_test_p1_v*_flag.txt
        + prompt 2: dbrd_test_p2_v*_flag.txt
        + no filtering: dbrd_test_p5_v*.txt
    - Hadoop
    - Kibana
```
put them under `data`

# Pipeline

## Extract duplicate BRs in test set
```bash
python prepare_data.py --project <project_name> --prompt <prompt>
```

## Run ChatGPT
```bash
python run_chatgpt.py --project <project_name> --prompt <prompt>
```

## Write data back
```bash
python generate_new_data.py --project <project_name> --prompt <prompt>
```

## Running REP
Please follow the instructions in [REP](https://github.com/irving-muller/fast-dbrd-modified) repo to run REP.

## RQ1
## Result
`result/Cupid`


## RQ2: Ablation Study
### Filtering Rules
Get the flag files:
```bash
python prepare_data.py --project spark --prompt 5
```
- (1) All, without filtering
- (2) length + content


### Prompt Template
- (1) With prompt 1
- (2) With prompt 2

## Baseline
For SABD and Siamese Pair, we directly report the results from [TOSEM-DBRD](https://github.com/soarsmu/TOSEM-DBRD) work as we used the same dataset.