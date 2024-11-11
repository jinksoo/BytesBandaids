import re
import ast  # To safely parse the dictionary-like input strings

# Define a function to calculate risk score from a data line
def calculate_risk_score(data_line):
    scores = {
        "diet": 0,
        "mental_health": 0,
        "medication_compliance": 0,
        "social_determinants": 0
    }
    original_lines = []  # To store relevant original lines for output

    # Dictionary to map keywords to score categories
    keyword_mapping = {
        "diet": "diet",
        "mental health": "mental_health",
        "medication compliance": "medication_compliance",
        "social determinants of health": "social_determinants"
    }
    
    # Parse dictionary string to extract relevant fields
    data_dict = ast.literal_eval(data_line)
    result_text = data_dict.get("result", "")

    # Iterate through each keyword and check for "Yes" or "No" in result
    for keyword, category in keyword_mapping.items():
        match = re.search(rf"{keyword}:\s*(Yes|No)", result_text, re.IGNORECASE)
        if match:
            response = match.group(1).strip().lower()
            if response == "yes":
                scores[category] += 1
            original_lines.append(f"{keyword}: {response.capitalize()}")  # Store original line with response

    # Calculate total risk score
    total_score = sum(scores.values())
    
    # Return total score and original lines as a formatted string for output
    output_lines = [f"Risk Score: {total_score}: {line}" for line in original_lines]
    return total_score, output_lines, data_line

# Define the main function to read, process, and append output line by line
def main():
    input_filename = "/Users/matthewjinsookim/Downloads/train_SDoHoutput.txt"  # Replace with your input file path
    output_filename = "/Users/matthewjinsookim/Downloads/PaRSoutput.txt"  # Replace with your desired output file path
    shortened_output_filename = "/Users/matthewjinsookim/Downloads/sPaRSoutput.txt" 
    
    with open(input_filename, 'r') as infile, open(output_filename, 'a') as outfile:
        for line in infile:
            line = line.strip()
            # Skip lines that start with an integer
            if line and not line[0].isdigit():
                # write original line it parses
                outfile.write(line + "\n")

                # Process each line to calculate score and formatted output
                total_score, output_lines, orig_line = calculate_risk_score(line)
                
                # Write to the output file
                outfile.write(f"Total Risk Score = {total_score}\n")
                for output_line in output_lines:
                    outfile.write(output_line + "\n")
                outfile.write("\n")  # Add newline for readability between records

    with open(input_filename, 'r') as infile, open(shortened_output_filename, 'a') as outfile:
        for line in infile:
            line = line.strip()
            # Skip lines that start with an integer
            if line and not line[0].isdigit():

                # Process each line to calculate score and formatted output
                total_score, output_lines, orig_line = calculate_risk_score(line)
                
                # Write to the output file
                outfile.write(f"Total Risk Score = {total_score}\n")
                for output_line in output_lines:
                    outfile.write(output_line + "\n")
                outfile.write("\n")  # Add newline for readability between records

    print(f"Processing complete. Output appended to {output_filename}")

# Run the main function
if __name__ == "__main__":
    main()
