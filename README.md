# DNABERT For Next Sentence Prediction

This project was about using a Natural Language Processing model for improving DNA assembly: 
One of the main challenges in genomics is the determination of genome sequence using sequenced DNA fragments called reads. The standard procedure is the construction of a graph from overlapping reads and finding a path through it. The path represents the final sequence. However, there are no exact algorithms that could accomplish this problem in a reasonable amount of time. Therefore, deep learning methods and reinforcement learning algorithms for graph simplifications are used in this project to develop suitable and efficient models for locating critical patterns in graphs. This project aimed to use a Natural Language Processing model for DNA assembly at nodes on the graph to predict the next sequence node, hence helping to simplify the graph.

## Features

- New subclass for sentence prediction
- Data preparation files for k-mers throught 3 different methods:
  - Non-overlapping  
  - Sliding window by k-mer
  - Sliding window by base
- Subreads mapping to reference genome

## Installation

Clone the [DNABERT repo](https://github.com/jerryji1993/DNABERT) and install the dependencies on the server.

```sh
git clone https://github.com/jerryji1993/DNABERT
cd DNABERT
python3 -m pip install --editable
cd examples
python3 -m pip install -r requirements.txt
```

Download the pretrained models from [here](https://github.com/jerryji1993/DNABERT#32-download-pre-trained-dnabert).

## Data Preparation w/o Mapping
Run `(k)mer_(method)_(train/dev)_(no. of records)rec.py` to generate the respective datasets. For example, `6mer_bybase_dev_200rec.py` will generate a `.tsv` file with:
- 6-mers
- Sliding window by base method
- An evaluation dataset (dev)
- Using 200 records from subreads

## Data Preparation w/ Mapping
Run `trim_ecoli_reference.py` to trim the original complete ecoli genome to 100,000 bases long. This generates `trimmed_100000.fasta`.

Execute the following command to get the matching output:

```sh
minimap2 -x map-hifi --secondary=no trimmed_100000.fasta SRR10971019.fastq > trimmed_mapping.paf
```

Use `filtered_0.9_bybase_3mer.py` to extract the records in `trimmed_mapping.paf` and generate the corresponding 3-mer datasets.

## Finetuning DNABERT Model
Use the respective datasets generated to finetune the pretrained DNABERT model downloaded previously.

Note: The task name for sentence prediction is "sp" (line 5).

```sh
python -u run_finetune_withdebugmessages.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name SP \
    --do_train \
    --do_eval \
    --data_dir $DATA_PATH \
    --max_seq_length 75 \
    --per_gpu_eval_batch_size=16   \
    --per_gpu_train_batch_size=16   \
    --learning_rate 2e-4 \
    --num_train_epochs 3.0 \
    --output_dir $OUTPUT_PATH \
    --evaluate_during_training \
    --logging_steps 100 \
    --save_steps 4000 \
    --warmup_percent 0.1 \
    --hidden_dropout_prob 0.1 \
    --overwrite_output \
    --weight_decay 0.01 \
    --n_process 8 > filtered_0.9_bybase_3mer.txt
```
