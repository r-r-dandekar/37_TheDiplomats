# Function to remove the first column from CSV data
def remove_first_column_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        rows = file.readlines()  # Read all lines from the file

    # Process each row to remove the first column
    cleaned_rows = [row.split(",”", 1)[1] if ",”" in row else row for row in rows]

    return cleaned_rows

# Function to save the cleaned data back to a new file
def save_cleaned_data(cleaned_data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for row in cleaned_data:
            file.write(row + '\n')  # Write each cleaned row to the file

# Main function
def main():
    input_file_path = 'C:\\Users\\dprut\\Downloads\\combined-small (2).csv'  # Path to the input CSV file
    output_file_path = 'cleaned_output_file.csv'  # Path to save the cleaned output

    # Remove the first column and get the cleaned data
    cleaned_data = remove_first_column_from_file(input_file_path)

    # Save the cleaned data to a new file
    save_cleaned_data(cleaned_data, output_file_path)
    print(f"Cleaned data saved to {output_file_path}")

# Call the main function
if __name__ == "__main__":
    main()
