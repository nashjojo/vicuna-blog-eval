"""
Convert jsonl file to csv file.

Usage:
1. input_file: input jsonl file
2. output_file: output csv file
"""
import json,csv

# parse arguments from command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', required=False, type=str, default="review.jsonl", help='input file')
parser.add_argument('--output_file', required=False, type=str, default="review.csv", help='ouput file')
args = parser.parse_args()

# function to load jsonl file
def load_file(input_file):
    with open(input_file, 'r') as f:
        # load json files line by line
        lines = f.readlines()
        # convert to json
        rows = [json.loads(line) for line in lines]
    return rows

if __name__ == '__main__':
    rows = load_file(args.input_file)
    with open(args.output_file, 'w') as outfile:
        # add a new field "gpt-4" to the output file
        csv_writer = csv.DictWriter(outfile, fieldnames=list(rows[0].keys()), delimiter=',', quotechar='"')
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)