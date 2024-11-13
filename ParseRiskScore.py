import re
import ast  # To safely parse the dictionary-like input strings

# Define a function to calculate risk score from a data line
def calculate_risk_score(data_line):
    scores = {
        "diet": 0,
        "mental_health": 0,
        "access_healthcare": 0,
        "social_support": 0
    }
    original_lines = []  # To store relevant original lines for output

    # Dictionary to map keywords to score categories
    keyword_mapping = {
        "diet": "diet",
        "mental health": "mental_health",
        "access to healthcare resources": "access_healthcare",
        "lack of social support": "social_support"
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
    output_lines = [f"Risk Score: {line}" for line in original_lines]
    return total_score, scores, output_lines, data_line

# Define the main function to read, process, and append output line by line
def main():
    input_filename = "/Users/matthewjinsookim/Downloads/combined_SDoHoutput.txt"  # Replace with your input file path
    output_filename = "/Users/matthewjinsookim/Downloads/combined_PaRSoutput.txt"  # Replace with your desired output file path
    shortened_output_filename = "/Users/matthewjinsookim/Downloads/combined_sPaRSoutput.txt"
    dfoutput_filename = "/Users/matthewjinsookim/Downloads/combined_df_PaRSoutput.txt"
    statistics_filename = "/Users/matthewjinsookim/Downloads/combined_statistics.txt"

    # Initialize counters for statistics
    one_yes_count = 0
    two_yes_count = 0
    three_or_more_yes_count = 0
    diet_yes_count = 0
    mental_health_yes_count = 0
    access_healthcare_yes_count = 0
    social_support_yes_count = 0
    total_lines = 0

    with open(input_filename, 'r') as infile, open(output_filename, 'a') as outfile:
        for line in infile:
            line = line.strip()
            # Skip lines that start with an integer
            if line and (line[0] != 'D'):
                total_lines += 1  # Count each valid line processed
                # write original line it parses
                outfile.write(line + "\n")

                # Process each line to calculate score and formatted output
                total_score, scores, output_lines, orig_line = calculate_risk_score(line)
                
                # Update category-specific counts
                diet_yes_count += scores["diet"]
                mental_health_yes_count += scores["mental_health"]
                access_healthcare_yes_count += scores["access_healthcare"]
                social_support_yes_count += scores["social_support"]

                # Update counters for number of "YES" responses
                if total_score == 1:
                    one_yes_count += 1
                elif total_score == 2:
                    two_yes_count += 1
                elif total_score >= 3:
                    three_or_more_yes_count += 1

                # Write to the output file
                outfile.write(f"Total Risk Score = {total_score}\n")
                for output_line in output_lines:
                    outfile.write(output_line + "\n")
                outfile.write("\n")  # Add newline for readability between records

    # Write statistics to a new file
    with open(statistics_filename, 'w') as stats_file:
        stats_file.write("Statistics:\n")
        stats_file.write(f"# of 1 YES: {one_yes_count}\n")
        stats_file.write(f"# of 2 YES: {two_yes_count}\n")
        stats_file.write(f"# of 3+ YES: {three_or_more_yes_count}\n")
        stats_file.write(f"# of diet YES: {diet_yes_count}\n")
        stats_file.write(f"# of mental health YES: {mental_health_yes_count}\n")
        stats_file.write(f"# of access to healthcare resources YES: {access_healthcare_yes_count}\n")
        stats_file.write(f"# of social support YES: {social_support_yes_count}\n")
        stats_file.write(f"Total number of lines: {total_lines}\n")

    with open(input_filename, 'r') as infile, open(shortened_output_filename, 'a') as outfile:
        for line in infile:
            line = line.strip()
            # Skip lines that start with an integer
            if line and (line[0] != 'D'):

                # Process each line to calculate score and formatted output
                total_score, scores, output_lines, orig_line = calculate_risk_score(line)

                # Write to the output file
                outfile.write(f"Total Risk Score = {total_score}\n")
                for output_line in output_lines:
                    outfile.write(output_line + "\n")
                outfile.write("\n")  # Add newline for readability between records

    print(f"Processing complete. Statistics written to {statistics_filename}")

# Run the main function
if __name__ == "__main__":
    main()
