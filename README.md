## Data


## Results


## Commands
### Generate input for REP
To run REP, we need prepare one file for each different json file: `dbrd_test.txt`. Go to `SABD` directory and run the following command:

```bash
python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_gpt_p1_r1.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_gpt_p1_r1.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_gpt_p1_r2.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_gpt_p1_r2.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_gpt_p1_r3.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_gpt_p1_r3.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_gpt_p1_r4.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_gpt_p1_r4.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_gpt_p1_r5.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_gpt_p1_r5.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_kpminer_test_1.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_kpminer.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_tfidf_test_1.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_tfidf.txt

python classical_approach/generate_input_dbrd.py --database ../data/keywords/spark/spark_yake_test_1.json --test ../data/raw/test_spark.txt --output ../data/rep/dbrd_test_spark_yake.txt
```

### Run REP

```bash
build/bin/fast-dbrd -n 20240508_spark_gpt_p1_r1 -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_gpt_p1_r1.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_gpt_p1_r2 -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_gpt_p1_r2.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_gpt_p1_r3 -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_gpt_p1_r3.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_gpt_p1_r4 -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_gpt_p1_r4.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_gpt_p1_r5 -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_gpt_p1_r5.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_kpminer -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_kpminer.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_tfidf -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_tfidf.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt

build/bin/fast-dbrd -n 20240508_spark_yake -r ranknet-configs/full-textual-no-version.cfg --ts /app/tosem-sampel-data/spark/timestamp_file.txt --time-constraint 365 --training-duplicates 273 --recommend /app/tosem-sampel-data/spark/dbrd_test_spark_yake.txt --trainfile /app/tosem-sampel-data/spark/sampled_training_spark_triplets_random_1.txt
```

## RQ1


## RQ2


## RQ3: Comparing with other keyword extraction methods
### LLMs
Running LLaMA 3 and Phi
path: `src/run_llm.ipynb`

Running OpenChat
Repo: https://github.com/imoneoi/openchat

```bash
CUDA_VISIBLE_DEVICES=2 python -m ochat.serving.openai_api_server --model openchat/openchat-3.5-0106'
```
We have deplpyed the API server and inference the model with the requests. There are 13 cases returning <Response [400]>, thus, we kept their original content.

### Specific keyword extraction methods
path: `src/run_pke.ipynb`

