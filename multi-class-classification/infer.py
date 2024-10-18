from transformers import DistilBertTokenizer
from transformers import AutoModelForSequenceClassification
from torch import nn, argmax
import numpy as np
import json

checkpoint = "distilbert-base-uncased"
SAVE_DIR="distilbert-finetuned-imdb-multi-label"
tokenizer = DistilBertTokenizer.from_pretrained(checkpoint)

# Loading the model
model = AutoModelForSequenceClassification.from_pretrained(SAVE_DIR)  # automatically loads the configuration.

with open('label_mapping.json', 'r') as f:
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

while True:
  # text = "Session: 30546354_3321642168 initialized by client WindowsUpdateAgent."
  text=input()
  print(infer(text))