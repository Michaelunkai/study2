from transformers import Trainer, TrainingArguments, BertForSequenceClassification, BertTokenizerFast
from datasets import load_dataset

# Load dataset
dataset = load_dataset('csv', data_files={'train': 'train.csv', 'test': 'test.csv'})

# Load pretrained model and tokenizer
model_name = "bert-base-uncased"
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizerFast.from_pretrained(model_name)

# Tokenize dataset
def preprocess(data):
    return tokenizer(data['text'], padding='max_length', truncation=True)

encoded_dataset = dataset.map(preprocess, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eva tion_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['test']
)

# Train the model
trainer.train()
