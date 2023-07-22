"""
Given an csv table with fields 
    Category	prompt_category	Q1	A1	Q2	A2	Q3	A3	"GPT-3.5:website"	"GPT-4:website"	"v0.2"	"v0.3:do_sample=True,temperature=0.7,top_p=1,top_k=50,no_repeat_ngram_size=4,"	"v0.3:do_sample=True,temperature=0.7,top_p=0.3,top_k=40,no_repeat_ngram_size=5,"

Generate the following jsonl files:
1. question.jsonl: {"question_id": 1, "text": "How can I improve my time management skills?", "category": "generic"}
2. answer_v0.3.jsonl: {"question_id": 1, "text": "Improving time management skills involves setting priorities, breaking tasks into smaller chunks, delegating tasks, avoiding multitasking, and taking regular breaks. Additionally, it is important to have a positive attitude and be realistic with goals. Making a to-do list, tracking time, and using technology to automate mundane tasks can also help improve time management skills.", "answer_id": "kEL9ifUHDeYuAXzevje2se", "model_id": "alpaca-13b:v1", "metadata": {"huggingface_argument": {"do_sample=True": treratureue, "temperature": 0.7, "top_p": 0.3, "top_k": 40, "no_repeat_ngram_size": 5}}}
    from the column "v0.3:do_sample=True,temperature=0.7,top_p=0.3,top_k=40,no_repeat_ngram_size=5,", where the model_id is v0.3, and the metadata is {"do_sample": true, "temperature": 0.7, "top_p": 0.3, "top_k": 40, "no_repeat_ngram_size": 5}
"""

import csv,json
import shortuuid

# model_ids = ["GPT-4:website", "v0.2", "v0.3:do_sample=True,temperature=0.7,top_p=1,top_k=50,no_repeat_ngram_size=4,", "v0.3:do_sample=True,temperature=0.7,top_p=0.3,top_k=40,no_repeat_ngram_size=5,"]
# Extrac only new model answers, to avoid duplicate answer_id. 

# parse arguments from command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', required=False, type=str, default="/Users/kaixiang.mo/Downloads/2023-05-31_LLM_eval_human_sense_v03.csv", help='input file')
parser.add_argument('--question', required=False, type=str, default=None, help='question in jsonl format.')
parser.add_argument('--answer', required=False, type=str, default=None, help='answer in jsonl format.')
parser.add_argument('--question_start_id', required=False, type=int, default=10000, help='answer starting id')
parser.add_argument('--model_ids', required=False, type=str, nargs='+', default=[], help='models to test')
args = parser.parse_args()

# function to load input file
def load_file(input_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        rows = [row for row in reader]
    return rows

if __name__ == '__main__':
    # load input file
    rows = load_file(args.input_file)

    # for each row, generate question and answer
    question_jsons = []
    answer_jsons = []
    for idx,row in enumerate(rows):
        question_id = args.question_start_id + idx+1
        question_text = row["Q1"]
        question_category = row["prompt_category"]
        question_json = {"question_id": question_id, "text": question_text, "category": question_category}
        question_jsons.append(question_json)

        for model_id in args.model_ids:
            answer_id = shortuuid.uuid()
            answer_text = row[model_id]
            # split the model_id into model_id and metadata
            model_version = model_id.split(":")[0]
            model_metadata = model_id.split(":")[1:]
            metadata_dict = {}
            for metadata in model_metadata:
                for metadata_parts in metadata.split(','):
                    if len(metadata_parts.strip())==0:
                        continue
                    try:
                        metadata_key = metadata_parts.split('=')[0]
                        metadata_value = metadata_parts.split('=')[1]
                        metadata_dict[metadata_key] = metadata_value
                    except:
                        print(f"error in metadata: {metadata_parts}")
            answer_metadata = {"huggingface_argument": metadata_dict}
            answer_json = {"question_id": question_id, "text": answer_text, "answer_id": answer_id, "model_id": model_id, "metadata": answer_metadata}
            answer_jsons.append(answer_json)
    
    # write to jsonl file
    if args.question is not None:
        with open(args.question, 'w') as f:
            for question_json in question_jsons:
                f.write(f"{json.dumps(question_json)}\n")

    # write to jsonl file according to model_id
    if args.answer is not None:
        with open(args.answer, 'w') as f:
            for answer_json in answer_jsons:
                f.write(f"{json.dumps(answer_json)}\n")