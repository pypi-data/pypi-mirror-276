import os
import pandas as pd
from transformers import DebertaTokenizer, DebertaForSequenceClassification, Trainer, TrainingArguments, TrainerCallback
import torch
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from datasets import Dataset
from sklearn.model_selection import train_test_split
from collections import Counter

# Set device to CPU
device = torch.device('cpu')

# Load dataset
df = pd.read_csv('/Users/kaleemullahqasim/Documents/GitHub/arxiv-paper-abstracts/arxiv_data.csv')
df = df.head(200)  # Select only the first 1000 rows

# Preprocess data: Create custom category columns
df['categories_list'] = df['terms'].apply(lambda x: x.split(','))

mlb = MultiLabelBinarizer()
labels = mlb.fit_transform(df['categories_list'].tolist())

# Convert DataFrame to a dictionary
data = {'summaries': df['summaries'].tolist(), 'labels': labels.tolist()}

# Tokenization
tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')

def preprocess_function(examples):
    output = tokenizer(examples['summaries'], truncation=True, padding=True, max_length=128)
    output['input_ids'] = output.pop('input_ids')  # Add input_ids to the output
    return output

# Load the dataset
dataset = Dataset.from_dict(data)

# Encode texts
dataset = dataset.map(preprocess_function, batched=True)

# Remove labels with only a single instance
label_counts = Counter([tuple(label) for label in dataset['labels']])
valid_labels = [label for label, count in label_counts.items() if count > 1]
dataset = dataset.filter(lambda example: tuple(example['labels']) in valid_labels)

# Split dataset into training and validation sets with stratification
summaries_train, summaries_test, labels_train, labels_test = train_test_split(
    dataset['summaries'], dataset['labels'], test_size=0.2, random_state=42, stratify=dataset['labels']
)

train_dataset = Dataset.from_dict({'summaries': summaries_train, 'labels': labels_train, 'input_ids': dataset['input_ids'][:len(summaries_train)]})
test_dataset = Dataset.from_dict({'summaries': summaries_test, 'labels': labels_test, 'input_ids': dataset['input_ids'][len(summaries_train):]})

# Load model and move to CPU
model = DebertaForSequenceClassification.from_pretrained('microsoft/deberta-base', num_labels=len(mlb.classes_))
model.to(device)

# Collect loss and f1-score for plotting
losses = []
f1_scores = []

# Define TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=10,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
)

# Custom metric for evaluation
def compute_metrics(eval_pred):
    logits = eval_pred.predictions
    labels = eval_pred.label_ids
    predictions = (torch.sigmoid(torch.Tensor(logits)) > 0.5).int()
    f1 = f1_score(torch.Tensor(labels).int().cpu().numpy(), predictions.cpu().numpy(), average='samples')
    return {"f1": f1}

# Custom callback to log losses and f1-scores
# class CustomCallback(TrainerCallback):
#     def on_log(self, args, state, control, logs=None, **kwargs):
#         losses.append(logs["eval_loss"])
#         f1_scores.append(logs["eval_f1"])


class CustomCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            losses.append(logs.get("eval_loss", 0.0))
            f1_scores.append(logs.get("eval_f1", 0.0))

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    callbacks=[CustomCallback()]
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./deberta_finetuned')
tokenizer.save_pretrained('./deberta_finetuned')
model.to('cpu')  # Ensure the model is on CPU

# Inference example
model.eval()
test_texts = [example['summaries'] for example in test_dataset]
predicted_categories = []

for text in test_texts:
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    encoded_input['input_ids'] = encoded_input.pop('input_ids')  # Add input_ids to the encoded_input
    encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
    output = model(**encoded_input)
    predictions = torch.sigmoid(output.logits).squeeze().detach().numpy()
    top_N = 3  # Change this to 4 or any other number you want
    top_labels = np.argsort(predictions)[-top_N:]  # Get the top N labels
    predicted_labels = [mlb.classes_[i] for i in top_labels]  # Get the corresponding labels
    predicted_categories.append(predicted_labels)

# Print abstracts with predicted labels
for abstract, labels in zip(test_texts, predicted_categories):
    print(f"Abstract: {abstract}\nPredicted Labels: {labels}\n")

# Plot training and validation metrics
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(losses, label='Validation Loss')
plt.title('Validation Loss per Epoch')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(f1_scores, label='Validation F1-Score')
plt.title('Validation F1-Score per Epoch')
plt.xlabel('Epoch')
plt.ylabel('F1-Score')
plt.legend()
plt.show()