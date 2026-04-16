import json
import os
import collections
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def print_confusion_matrix(matrix, labels):
    """
    Prints a formatted confusion matrix.
    """
    print("\nConfusion Matrix:")
    header = "True \\ Pred".ljust(12)
    for label in labels:
        header += label.center(10)
    print(header)
    print("-" * len(header))
    
    for i, row in enumerate(matrix):
        line = labels[i].ljust(12)
        for val in row:
            line += str(val).center(10)
        print(line)

def run_evaluation(results_file="results_output.json"):
    """
    Reads the results file and calculates evaluation metrics.
    """
    if not os.path.exists(results_file):
        print(f"Error: Results file '{results_file}' not found. Please run the batch processing script first.")
        return

    # 1. Load data
    try:
        with open(results_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {results_file}: {e}")
        return

    if not data:
        print("Error: Results file is empty.")
        return

    # 2. Extract valid predictions and ground truths
    y_true = []
    y_pred = []
    errors = 0
    valid_pmids = []

    # Expected labels
    target_labels = ["yes", "no", "maybe"]

    for item in data:
        gt = item.get("ground_truth")
        pred = item.get("prediction")
        pmid = item.get("pmid")

        if pred == "error" or pred not in target_labels:
            errors += 1
            continue
            
        if gt not in target_labels:
            # If ground truth is something else, we might need to skip or map it
            continue

        y_true.append(gt)
        y_pred.append(pred)
        valid_pmids.append(pmid)

    if not y_pred:
        print("Error: No valid predictions found to evaluate.")
        return

    # 3. Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    # Classification Report
    # We specify labels to ensure they are in the correct order in the matrix
    labels = target_labels
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    # 4. Print Results
    print("=" * 60)
    print("LLM EVALUATION REPORT")
    print("=" * 60)
    print(f"Total samples processed: {len(data)}")
    print(f"Valid samples for evaluation: {len(y_pred)}")
    print(f"Errors/Failed calls: {errors}")
    print(f"Overall Accuracy: {accuracy:.4f}")
    print("-" * 60)
    print("\nDetailed Metrics:")
    print(report)
    
    print_confusion_matrix(cm, labels)
    print("=" * 60)

    # 5. Distribution analysis
    print("\nPrediction Distribution:")
    pred_counts = collections.Counter(y_pred)
    total_valid = len(y_pred)
    for label in target_labels:
        count = pred_counts.get(label, 0)
        print(f"  {label.ljust(6)}: {count} ({count/total_valid*100:6.2f}%)")
    
    print("\nGround Truth Distribution:")
    gt_counts = collections.Counter(y_true)
    for label in target_labels:
        count = gt_counts.get(label, 0)
        print(f"  {label.ljust(6)}: {count} ({count/total_valid*100:6.2f}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_evaluation("results_test_output.json")
