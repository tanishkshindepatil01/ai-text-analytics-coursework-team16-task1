import json
import random
import math
from functools import reduce
from collections import defaultdict
from config import CFG
import os

def split_dataset_logic(dataset_pmids, labels, fold):
    """Ported from reference notebook for consistency."""
    add = lambda x: reduce(lambda a, b: a + b, x)

    label2pmids = defaultdict(list)
    for pmid, lab in zip(dataset_pmids, labels):
        label2pmids[lab].append(pmid)

    label2splits = {}
    for lab, pmids in label2pmids.items():
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

    # Adjust sizes if needed to match notebook behavior
    if len(output[-1]) != len(output[0]):
        for i in range(fold - 1):
            if len(output[i]) > len(output[-1]):
                picked = random.choice(output[i])
                output[-1].append(picked)
                output[i].remove(picked)

    return output

def split_dataset(json_path: str = "processed_pubmedqa.json"):
    """
    Splits the dataset into 500 CV samples and 500 Test samples.
    Then prepares 10 folds for the CV set.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Prepare data for splitting
    pmids = [item['pmid'] for item in data]
    labels = [item['final_decision'] for item in data]
    
    # 2. Initial Split: 500/500 (CV : Test)
    # Replicating notebook seed and logic
    random.seed(0)
    two_halves = split_dataset_logic(pmids, labels, 2)
    
    cv_pmids = set(two_halves[0])
    test_pmids = set(two_halves[1])
    
    print(f"Total samples: {len(data)}")
    print(f"CV samples: {len(cv_pmids)}")
    print(f"Test samples: {len(test_pmids)}")
    
    cv_data = [item for item in data if item['pmid'] in cv_pmids]
    test_data = [item for item in data if item['pmid'] in test_pmids]
    
    # 3. 10-Fold Cross Validation on CV set
    random.seed(0)
    cv_labels = [item['final_decision'] for item in cv_data]
    cv_pmid_list = [item['pmid'] for item in cv_data]
    
    ten_folds = split_dataset_logic(cv_pmid_list, cv_labels, 10)
    
    pmid_to_fold = {}
    for fold_idx, fold_pmids in enumerate(ten_folds):
        for pmid in fold_pmids:
            pmid_to_fold[pmid] = fold_idx
            
    # Add fold info to cv_data
    for item in cv_data:
        item['fold'] = pmid_to_fold[item['pmid']]
    
    # Save the splits
    splits = {
        'test': test_data,
        'cv': cv_data
    }
    
    with open('dataset_splits.json', 'w', encoding='utf-8') as f:
        json.dump(splits, f, ensure_ascii=False, indent=4)
    
    print("Dataset splits saved to dataset_splits.json")
    for i in range(10):
        fold_size = len([item for item in cv_data if item['fold'] == i])
        print(f"Fold {i}: {fold_size} samples")
        
    return splits

if __name__ == "__main__":
    # Check if processed file exists, else use ori_pqal.json
    if not os.path.exists("processed_pubmedqa.json"):
        print("Warning: processed_pubmedqa.json not found. Using ori_pqal.json directly.")
        with open("ori_pqal.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        data = []
        for pmid, info in raw_data.items():
            data.append({
                "pmid": pmid,
                "final_decision": info["final_decision"],
                "QUESTION": info.get("QUESTION", ""),
                "CONTEXTS": info.get("CONTEXTS", []),
                "LONG_ANSWER": info.get("LONG_ANSWER", "")
            })
        with open("processed_pubmedqa.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    split_dataset("processed_pubmedqa.json")
