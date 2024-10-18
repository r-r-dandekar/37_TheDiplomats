import pandas as pd
import json
# df = pd.read_csv("IMDB-Movie-Data.csv", usecols=["Content", "Level"])
CSV_PATH="combined-small.csv"
SAVE_DIR="distilbert-finetuned-imdb-multi-label"
df = pd.read_csv(CSV_PATH, usecols=["Content", "Level"])

# Get the unique values from the 'Level' column, maintaining order of appearance
unique_values = pd.unique(df['Level'])
# Create a dictionary that maps each unique value to an index based on its position
level_dict = {idx: value for idx, value in enumerate(unique_values)}
# Output the dictionary
with open('label_mapping.json', 'w') as f:
    json.dump(level_dict, f)

df.duplicated().sum()
# df['Content'].str.len().plot.hist(bins=50)
df['Level'] = df['Level'].str.split(',')
level_counts = [g for gen in df['Level'] for g in gen]
pd.Series(level_counts).value_counts()

from sklearn.preprocessing import MultiLabelBinarizer
multilabel = MultiLabelBinarizer()

labels = multilabel.fit_transform(df['Level']).astype('float32')

texts = df['Content'].tolist()

labels
texts[:5]
import torch
from transformers import DistilBertTokenizer, AutoTokenizer
from transformers import AutoModelForSequenceClassification, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels,
                                                                    test_size=0.2, random_state=42)


checkpoint = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=len(labels[0]),
                                                            problem_type="multi_label_classification")
labels[0]
# Lets build custom dataset
class CustomDataset(Dataset):
  def __init__(self, texts, labels, tokenizer, max_len=128):
    self.texts = texts
    self.labels = labels
    self.tokenizer = tokenizer
    self.max_len = max_len

  def __len__(self):
    return len(self.texts)

  def __getitem__(self, idx):
    text = str(self.texts[idx])
    label = torch.tensor(self.labels[idx])

    encoding = self.tokenizer(text, truncation=True, padding="max_length", max_length=self.max_len, return_tensors='pt')   

    return {
        'input_ids': encoding['input_ids'].flatten(),
        'attention_mask': encoding['attention_mask'].flatten(),
        'labels': label
    }


train_dataset = CustomDataset(train_texts, train_labels, tokenizer)
val_dataset = CustomDataset(val_texts, val_labels, tokenizer)
# val_dataset[0]
# Multi-Label Classification Evaluation Metrics
import numpy as np
from sklearn.metrics import roc_auc_score, f1_score, hamming_loss
from transformers import EvalPrediction
import torch


def multi_labels_metrics(predictions, labels, threshold=0.3):
  sigmoid = torch.nn.Sigmoid()
  probs = sigmoid(torch.Tensor(predictions))

  y_pred = np.zeros(probs.shape)
  y_pred[np.where(probs>=threshold)] = 1
  y_true = labels

  f1 = f1_score(y_true, y_pred, average = 'macro')
  roc_auc = roc_auc_score(y_true, y_pred, average = 'macro')
  hamming = hamming_loss(y_true, y_pred)

  metrics = {
      "roc_auc": roc_auc,
      "hamming_loss": hamming,
      "f1": f1
  }

  return metrics

def compute_metrics(p:EvalPrediction):
  preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions

  result = multi_labels_metrics(predictions=preds,
                                labels=p.label_ids)

  return result
# Training Arguments
from transformers import TrainingArguments, Trainer

args = TrainingArguments(
    per_device_train_batch_size=2, #Original 8
    per_device_eval_batch_size=2, #Original 8
    output_dir = './results',
    num_train_epochs=5, #Original 5
    save_steps=10, #Original 1000
    save_total_limit=2
)

trainer = Trainer(model=model,
                  args=args,
                  train_dataset=train_dataset,
                  eval_dataset = val_dataset,
                  compute_metrics=compute_metrics)
trainer.train()
# trainer.evaluate()
trainer.save_model(SAVE_DIR)
import pickle
with open("multi-label-binarizer.pkl", "wb") as f:
  pickle.dump(multilabel, f)
#!zip -r distilbert.zip "/content/distilbert-finetuned-imdb-multi-label"
text = "Carol Danvers gets her powers entangled with those of Kamala Khan and Monica Rambeau, forcing them to work together to save the universe."

encoding = tokenizer(text, return_tensors='pt')
encoding.to(trainer.model.device)

outputs = trainer.model(**encoding)
sigmoid = torch.nn.Sigmoid()
probs = sigmoid(outputs.logits[0].cpu())
preds = np.zeros(probs.shape)
preds[np.where(probs>=0.3)] = 1

multilabel.classes_

multilabel.inverse_transform(preds.reshape(1,-1))
preds.reshape(1,-1)


