import json
import pandas as pd

def merge_jsonl_files(file1, file2, output_file):
    data = []

    # Read and append data from the first JSONL file
    with open(file1, 'r') as f1:
        for line in f1:
            data.append(json.loads(line))

    # Read and append data from the second JSONL file
    with open(file2, 'r') as f2:
        for line in f2:
            data.append(json.loads(line))

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Save the merged data to a new JSONL file
    with open(output_file, 'w') as out_file:
        for record in df.to_dict(orient='records'):
            out_file.write(json.dumps(record) + '\n')

    print(f"Merged data saved to {output_file}")

# Usage
merge_jsonl_files('data/aci_train.jsonl', 'data/aci_test.jsonl', 'data/aci_combined.jsonl')