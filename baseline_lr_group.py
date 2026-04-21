import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report
from config import CFG

def load_splits(path='dataset_splits.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_10fold_cv(make_pipeline_fn, cv_df, text_col, test_texts, y_test,
                      n_folds=10):
    """
    Ported from reference notebook. Fits TF-IDF inside each fold.
    """
    fold_accs = []
    fold_f1s = []

    for fold_idx in range(n_folds):
        val_mask = cv_df["fold"] == fold_idx
        train_mask = ~val_mask

        X_tr = cv_df.loc[train_mask, text_col].tolist()
        y_tr = cv_df.loc[train_mask, "label_id"].values
        X_val = cv_df.loc[val_mask, text_col].tolist()
        y_val = cv_df.loc[val_mask, "label_id"].values

        pipe = make_pipeline_fn()
        pipe.fit(X_tr, y_tr)
        val_preds = pipe.predict(X_val)

        fold_accs.append(accuracy_score(y_val, val_preds))
        fold_f1s.append(f1_score(y_val, val_preds, average="macro"))

    # Final fit on all CV data to evaluate on test set
    final_pipe = make_pipeline_fn()
    X_cv_all = cv_df[text_col].tolist()
    y_cv_all = cv_df["label_id"].values
    final_pipe.fit(X_cv_all, y_cv_all)
    
    test_preds = final_pipe.predict(test_texts)
    test_acc = accuracy_score(y_test, test_preds)
    test_f1 = f1_score(y_test, test_preds, average="macro")

    return {
        "cv_acc_mean": np.mean(fold_accs),
        "cv_acc_std": np.std(fold_accs),
        "cv_f1_mean": np.mean(fold_f1s),
        "cv_f1_std": np.std(fold_f1s),
        "test_acc": test_acc,
        "test_f1": test_f1,
        "report": classification_report(y_test, test_preds, target_names=["no", "maybe", "yes"])
    }

def make_baseline_pipe():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True, stop_words="english",
            ngram_range=(1, 2), max_features=30000
        )),
        ("lr", LogisticRegression(
            class_weight="balanced", random_state=CFG.SEED, max_iter=1000
        ))
    ])

def run_baseline():
    splits = load_splits()
    cv_df = pd.DataFrame(splits['cv'])
    test_df = pd.DataFrame(splits['test'])
    
    y_test = test_df["label_id"].values
    X_test_qctx = test_df["q_ctx"].tolist()
    
    print("============================================================")
    print("BASELINE: TF-IDF (1,2)-grams + Logistic Regression")
    print("Protocol: 10-Fold CV on 500 samples, Test on 500 samples")
    print("============================================================")
    
    results = evaluate_10fold_cv(
        make_baseline_pipe, 
        cv_df, 
        "q_ctx", 
        X_test_qctx, 
        y_test
    )
    
    print(f"10-Fold CV Accuracy : {results['cv_acc_mean']:.4f} ± {results['cv_acc_std']:.4f}")
    print(f"10-Fold CV Macro-F1 : {results['cv_f1_mean']:.4f} ± {results['cv_f1_std']:.4f}")
    print(f"Test Accuracy       : {results['test_acc']:.4f}")
    print(f"Test Macro-F1       : {results['test_f1']:.4f}")
    print("\nTest Classification Report:")
    print(results['report'])

if __name__ == "__main__":
    run_baseline()
