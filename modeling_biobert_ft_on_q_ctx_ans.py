import os
import json
import random
import numpy as np
import pandas as pd
import torch
from collections import Counter
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    Trainer, 
    TrainingArguments, 
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, f1_score, classification_report


RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# Load data
def load_data():
    with open('dataset_splits.json', 'r', encoding='utf-8') as f:
        splits = json.load(f)
    
    cv_df = pd.DataFrame(splits['cv'])
    test_df = pd.DataFrame(splits['test'])
    
    dev_fold_mask = cv_df["fold"] == 0
    train_fold_mask = ~dev_fold_mask

    # uses q_ctx_ans
    train_texts = cv_df.loc[train_fold_mask, "text_q_ctx_ans"].tolist()
    train_labels = cv_df.loc[train_fold_mask, "label_id"].values.tolist()
    
    val_texts = cv_df.loc[dev_fold_mask, "text_q_ctx_ans"].tolist()
    val_labels = cv_df.loc[dev_fold_mask, "label_id"].values.tolist()
    
    test_texts = test_df["text_q_ctx_ans"].tolist()
    test_labels = test_df["label_id"].values.tolist()
    
    return train_texts, train_labels, val_texts, val_labels, test_texts, test_labels


# Dataset and weights
class QADataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=384):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = self.tokenizer(
            str(self.texts[idx]),
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )
        item = {k: v.squeeze(0) for k, v in enc.items()}
        item["labels"] = torch.tensor(int(self.labels[idx]), dtype=torch.long)
        return item

def get_class_weights(labels):
    counts = Counter(labels)
    total = len(labels)
    n_classes = 3
    weights = [total / (n_classes * counts[i]) for i in range(n_classes)]
    return torch.tensor(weights, dtype=torch.float32).to(device)

class WeightedTrainer(Trainer):
    def __init__(self, class_weights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels").to(model.device)
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fn = torch.nn.CrossEntropyLoss(weight=self.class_weights)
        loss = loss_fn(logits, labels)
        return (loss, outputs) if return_outputs else loss

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro")
    }

# Run training
def run_finetuning():
    MODEL_NAME = "dmis-lab/biobert-base-cased-v1.2"
    MAX_LEN = 384
    BATCH_SIZE = 8
    EPOCHS = 8
    LEARNING_RATE = 2e-5 
    
    tr_txt, tr_lbl, val_txt, val_lbl, ts_txt, ts_lbl = load_data()
    weights = get_class_weights(tr_lbl)
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3).to(device)
    
    train_ds = QADataset(tr_txt, tr_lbl, tokenizer, MAX_LEN)
    val_ds = QADataset(val_txt, val_lbl, tokenizer, MAX_LEN)
    test_ds = QADataset(ts_txt, ts_lbl, tokenizer, MAX_LEN)
    
    steps_per_epoch = max(1, len(train_ds) // BATCH_SIZE)
    total_steps = steps_per_epoch * EPOCHS
    warmup_steps = int(0.1 * total_steps)

    training_args = TrainingArguments(
        output_dir="./biobert_output",
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        weight_decay=0.01,
        warmup_steps=warmup_steps,
        report_to="none",
        fp16=True,
        save_total_limit=2
    )
    
    trainer = WeightedTrainer(
        class_weights=weights,
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    print("\nStarting BioBERT Fine-tuning (Identical to Notebook)...")
    trainer.train()
    
    print("\nEvaluating on Test Set...")
    test_results = trainer.predict(test_ds)
    preds = np.argmax(test_results.predictions, axis=1)
    
    print("\nFinal Results:")
    print(f"Accuracy: {accuracy_score(ts_lbl, preds):.4f}")
    print(f"Macro F1: {f1_score(ts_lbl, preds, average='macro'):.4f}")
    print("\nClassification Report:")
    print(classification_report(ts_lbl, preds, target_names=["no", "maybe", "yes"]))

if __name__ == "__main__":
    run_finetuning()
