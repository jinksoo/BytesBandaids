import pandas as pd
import re
import json

import pandas as pd
import re
import json



def load_data(dataset_file):
    # Load the JSONL file into a DataFrame
    data = []
    if dataset_file.endswith('.jsonl'):
        with open(dataset_file, "r") as file:
            for line in file:
                data.append(json.loads(line))
        df = pd.DataFrame(data)
    elif dataset_file.endswith('.csv'):
            df = pd.read_csv(dataset_file)
    else:
        raise ValueError("Unsupported file format. Please use .jsonl or .csv.")
    return df

# Define functions to extract dialogues
def extract_doctor_dialogue(text):
    if 'aci' in dataset_file:
        matches = re.findall(r"\[doctor\](.*?)(?=\[patient\]|\Z)", text, re.DOTALL)
       
    elif 'MTS' in dataset_file:
        matches = re.findall(r"Doctor:\s*(.*?)(?=Patient:|\Z)", text, re.DOTALL)

    return ' '.join(matches).strip() if matches else None

def extract_patient_dialogue(text):
    if 'aci' in dataset_file:
        matches = re.findall(r"\[patient\](.*?)(?=\[doctor\]|\Z)", text, re.DOTALL)
    elif 'MTS' in dataset_file:
        matches = re.findall(r"Patient:\s*(.*?)(?=Doctor:|\Z)", text, re.DOTALL)  
    return ' '.join(matches).strip() if matches else None

# Specify input file here
dataset_file = "data/mts-dialog/MTS_Dataset_TrainingSet.csv"
df = load_data(dataset_file)

# Apply the functions to extract dialogues and add as new columns
df['doctor_dialogue'] = df['dialogue'].apply(extract_doctor_dialogue)
df['patient_dialogue'] = df['dialogue'].apply(extract_patient_dialogue)

print(df['patient_dialogue'])