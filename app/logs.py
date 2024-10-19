from transformers import DistilBertTokenizer
from transformers import AutoModelForSequenceClassification
from torch import nn, argmax
import numpy as np
import json

checkpoint = "distilbert-base-uncased"
SAVE_DIR="models/distilbert"
tokenizer = DistilBertTokenizer.from_pretrained(checkpoint)

# Loading the model
model = AutoModelForSequenceClassification.from_pretrained(SAVE_DIR)  # automatically loads the configuration.

with open('models/distilbert/label_mapping.json', 'r') as f:
    idx2label = json.load(f)

def infer(text):
    encoding = tokenizer(text, return_tensors='pt')
    encoding.to(model.device)

    outputs = model(**encoding)
    sigmoid = nn.Sigmoid()
    probs = sigmoid(outputs.logits[0].cpu())
    i = argmax(probs).item()
    label = idx2label[str(i)]

    return label

def showlogs(path, main_window, result_queue):
    list = read_file_to_list(path)
    for string in list:
        level = infer(string)
        print(level, " ", string)
        result_queue.put((level, string))
    
        

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

if __name__ == "__main__":
    while True:
        # text = "Session: 30546354_3321642168 initialized by client WindowsUpdateAgent."
        text=input()
        print(infer(text))