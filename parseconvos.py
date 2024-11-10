import pandas as pd
import re
import json

# Load the JSONL file into a DataFrame
data = []

# Specify input file here
dataset_file = "/Users/laurachen/Documents/Github/clinical_visit_note_summarization_corpus/aci_train.jsonl"

with open(dataset_file, "r") as file:
    for line in file:
        data.append(json.loads(line))
df = pd.DataFrame(data)

# Define functions to extract dialogues
def extract_doctor_dialogue(text):
    matches = re.findall(r"\[doctor\](.*?)(?=\[patient\]|\Z)", text, re.DOTALL)
    return ' '.join(matches).strip() if matches else None

def extract_patient_dialogue(text):
    matches =re.findall(r"\[patient\](.*?)(?=\[doctor\]|\Z)", text, re.DOTALL)
    return ' '.join(matches).strip() if matches else None

# Apply the functions to extract dialogues and add as new columns
df['doctor_dialogue'] = df['dialogue'].apply(extract_doctor_dialogue)
df['patient_dialogue'] = df['dialogue'].apply(extract_patient_dialogue)

# Display the result
print(df[['doctor_dialogue', 'patient_dialogue']].head())