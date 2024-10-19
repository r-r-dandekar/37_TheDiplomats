import subprocess

def cmd_emulator():
    print("Simple CMD Emulator. Type 'exit' to quit.")
    while True:
        command = input("CMD> ")  # Get command from user
        if command.lower() in ['exit', 'quit']:  # Exit command
            break
        
        # Run the command
        process = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        # Print the output
        print(process.stdout)  # Output from the command
        if process.stderr:
            print("ERROR:\n", process.stderr)  # Errors, if any

if __name__ == "__main__":
    cmd_emulator()
