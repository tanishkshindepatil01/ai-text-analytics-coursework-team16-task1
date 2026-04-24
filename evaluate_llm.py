import json
import os
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score, f1_score
from data_prepocessor import DataPreprocessor

def run_evaluation(results_file="results_llm_test.json"):
    """
    Reads the results file and calculates evaluation metrics in the same way as baseline_lr_group.py.
    """
    if not os.path.exists(results_file):
        print(f"Error: Results file '{results_file}' not found.")
        return

    # 1. Load results
    try:
        with open(results_file, "r") as f:
            results_data = json.load(f)
    except Exception as e:
        print(f"Error loading {results_file}: {e}")
        return

    if not results_data:
        print("Error: Results file is empty.")
        return

    # 2. Extract predictions and ground truths
    processor = DataPreprocessor()
    # Mapping: {"no": 0, "maybe": 1, "yes": 2}
    
    y_true_ids = []
    y_pred_ids = []
    valid_count = 0
    error_count = 0

    for item in results_data:
        gt_label = item.get("ground_truth")
        pred_label = item.get("prediction")
        
        if pred_label == "error" or pred_label not in processor.label2id:
            error_count += 1
            continue
            
        y_true_ids.append(processor.label2id.get(gt_label))
        y_pred_ids.append(processor.label2id.get(pred_label))
        valid_count += 1

    if not y_pred_ids:
        print("Error: No valid predictions found to evaluate.")
        return

    # 3. Calculate metrics (Same as baseline_lr_group)
    test_acc = accuracy_score(y_true_ids, y_pred_ids)
    test_f1 = f1_score(y_true_ids, y_pred_ids, average="macro")
    report = classification_report(
        y_true_ids, 
        y_pred_ids, 
        target_names=["no", "maybe", "yes"],
        zero_division=0
    )

    # 4. Print Results in the same format as baseline_lr_group
    print("============================================================")
    print("LLM API EVALUATION (Zero-Shot)")
    print(f"Protocol: Evaluate on {valid_count} test samples")
    if error_count > 0:
        print(f"Note: {error_count} samples were skipped due to API errors.")
    print("============================================================")
    
    print(f"Test Accuracy       : {test_acc:.4f}")
    print(f"Test Macro-F1       : {test_f1:.4f}")
    print("\nTest Classification Report:")
    print(report)
    print("============================================================")

if __name__ == "__main__":
    run_evaluation("results_llm_test.json")
