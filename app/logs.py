def showlog(path):
    list = read_file_to_list(path)
    print("helo")

def read_file_to_list(file_path):
    """Reads a file and stores each line as an element in a list."""
    lines = []
    try:
        with open(file_path, 'r') as file:  # Open the file in read mode
            lines = file.readlines()  # Read all lines into a list
            lines = [line.strip() for line in lines]  # Remove newline characters
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return lines