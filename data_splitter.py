import json
import random
import math
import pandas as pd
from functools import reduce
from collections import defaultdict
from sklearn.model_selection import StratifiedKFold
import os

def split_dataset_logic(dataset_pmids, labels, fold):
    """Ported from reference notebook for consistency."""
    add = lambda x: reduce(lambda a, b: a + b, x)

    label2pmids = defaultdict(list)
    for pmid, lab in zip(dataset_pmids, labels):
        label2pmids[lab].append(pmid)

    label2splits = {}
    for lab, pmids in label2pmids.items():
        pmids = pmids.copy() # Match snippet copy behavior
        random.shuffle(pmids)
        num_all = len(pmids)
        num_split = math.ceil(num_all / fold)
        splits = []
        for i in range(fold):
            if i == fold - 1:
                splits.append(pmids[i * num_split:])
            else:
                splits.append(pmids[i * num_split: (i + 1) * num_split])
        label2splits[lab] = splits

    output = []
    for i in range(fold):
        fold_pmids = add([label2splits[lab][i] for lab in sorted(label2splits.keys())])
        output.append(fold_pmids)

    # Adjust sizes if needed to match notebook behavior (using while as in snippet)
    if len(output[-1]) != len(output[0]):
        for i in range(fold - 1):
            while len(output[i]) > len(output[-1]):
                picked = random.choice(output[i])
                output[-1].append(picked)
                output[i].remove(picked)

    return output

def split_dataset(json_path: str = "processed_pubmedqa.json"):
    """
    Splits the dataset into 500 CV samples and 500 Test samples.
    Then prepares 10 folds for the CV set using StratifiedKFold.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Prepare data for splitting
    pmids = [item['pmid'] for item in data]
    labels = [item['final_decision'] for item in data]
    
    # 2. Initial Split: 500/500 (CV : Test)
    random.seed(42)
    two_halves = split_dataset_logic(pmids, labels, 2)
    
    cv_pmids = set(two_halves[0])
    test_pmids = set(two_halves[1])
    
    print(f"Total samples: {len(data)}")
    print(f"CV samples: {len(cv_pmids)}")
    print(f"Test samples: {len(test_pmids)}")
    
    cv_data = [item for item in data if item['pmid'] in cv_pmids]
    test_data = [item for item in data if item['pmid'] in test_pmids]
    
    # 3. 10-Fold Cross Validation on CV set (Aligned with Snippet)
    cv_df = pd.DataFrame(cv_data)
    
    # Replicate snippet shuffling
    cv_df = cv_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Use StratifiedKFold as in snippet
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    
    cv_df["fold"] = -1
    for fold_idx, (_, val_idx) in enumerate(skf.split(cv_df, cv_df["final_decision"])):
        cv_df.loc[val_idx, "fold"] = fold_idx
        
    # Convert back to list of dicts for the split dictionary
    cv_data_aligned = cv_df.to_dict('records')
    
    # Save the splits
    splits = {
        'test': test_data,
        'cv': cv_data_aligned
    }
    
    with open('dataset_splits.json', 'w', encoding='utf-8') as f:
        json.dump(splits, f, ensure_ascii=False, indent=4)
    
    print("Dataset splits saved to dataset_splits.json (Aligned with Snippet)")
    for i in range(10):
        fold_size = len([item for item in cv_data_aligned if item['fold'] == i])
        print(f"Fold {i}: {fold_size} samples")
        
    return splits

if __name__ == "__main__":
    # Check if processed file exists
    if not os.path.exists("processed_pubmedqa.json"):
        print("Error: processed_pubmedqa.json not found. Run data_preprocessor first.")
    else:
        split_dataset("processed_pubmedqa.json")
