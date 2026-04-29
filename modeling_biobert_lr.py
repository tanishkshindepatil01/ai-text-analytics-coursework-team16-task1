import os
import json
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
from config import CFG
from tqdm import tqdm

def load_data(path='dataset_splits.json'):
    """Loads the official dataset splits."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset splits file not found at {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        splits = json.load(f)
    
    cv_df = pd.DataFrame(splits['cv'])
    test_df = pd.DataFrame(splits['test'])
    return cv_df, test_df

def get_embeddings(texts, model_name, batch_size=16):
    """
    Extracts frozen embeddings using a Transformer model and mean pooling.
    This replaces SentenceTransformer functionality if the library is missing.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    model.eval()
    
    all_embeddings = []
    
    for i in tqdm(range(0, len(texts), batch_size), desc=f"Encoding with {model_name}"):
        batch_texts = texts[i:i+batch_size]
        # Same MAX_LEN as the rest of the project
        encoded_input = tokenizer(
            batch_texts, 
            padding=True, 
            truncation=True, 
            max_length=384, 
            return_tensors='pt'
        ).to(device)
        
        with torch.no_grad():
            model_output = model(**encoded_input)
            
        # Perform Mean Pooling (Standard for sentence embeddings)
        attention_mask = encoded_input['attention_mask']
        token_embeddings = model_output[0] # Last hidden state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        mean_embeddings = sum_embeddings / sum_mask
        
        all_embeddings.append(mean_embeddings.cpu().numpy())
        
    return np.vstack(all_embeddings)

def run_biobert_lr_experiment():
    """
    Implements A1d: BioBERT Embeddings + LR.
    Frozen representations are used with a Logistic Regression classifier.
    """
    print("--- BioBERT Embeddings + Logistic Regression (A1d) ---")
    
    cv_df, test_df = load_data()
    
    y_cv = cv_df["label_id"].values
    y_test = test_df["label_id"].values
    
    # Protocol A1d: Uses Question + Context
    X_cv_text = cv_df["q_ctx"].tolist()
    X_test_text = test_df["q_ctx"].tolist()
    
    # Using the specialized BioBERT model for sentence embeddings used in the group notebook
    MODEL_NAME = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"
    
    print("\nPhase 1: Embedding Extraction")
    X_cv_emb = get_embeddings(X_cv_text, MODEL_NAME)
    X_test_emb = get_embeddings(X_test_text, MODEL_NAME)
    
    print("\nPhase 2: 10-Fold Cross-Validation")
    fold_f1s = []
    
    for fold_idx in range(10):
        val_mask = cv_df["fold"] == fold_idx
        train_mask = ~val_mask
        
        X_tr, y_tr = X_cv_emb[train_mask], y_cv[train_mask]
        X_val, y_val = X_cv_emb[val_mask], y_cv[val_mask]
        
        # Consistent with report and notebook settings
        clf = LogisticRegression(
            max_iter=3000, 
            class_weight="balanced", 
            random_state=CFG.SEED
        )
        clf.fit(X_tr, y_tr)
        preds = clf.predict(X_val)
        
        f1 = f1_score(y_val, preds, average="macro", zero_division=0)
        fold_f1s.append(f1)
        print(f"  Fold {fold_idx}: Macro-F1 = {f1:.4f}")
        
    print(f"\nCV Results: Mean Macro-F1 = {np.mean(fold_f1s):.4f} ± {np.std(fold_f1s):.4f}")
    
    print("\nPhase 3: Final Test Evaluation")
    final_clf = LogisticRegression(
        max_iter=3000, 
        class_weight="balanced", 
        random_state=CFG.SEED
    )
    final_clf.fit(X_cv_emb, y_cv)
    test_preds = final_clf.predict(X_test_emb)
    
    print("\nFinal Report (A1d):")
    print(f"Test Accuracy: {accuracy_score(y_test, test_preds):.4f}")
    print(f"Test Macro-F1: {f1_score(y_test, test_preds, average='macro', zero_division=0):.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(
        y_test, test_preds, 
        target_names=["no", "maybe", "yes"], 
        zero_division=0
    ))

if __name__ == "__main__":
    run_biobert_lr_experiment()
