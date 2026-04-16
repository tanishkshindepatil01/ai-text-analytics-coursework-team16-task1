import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack
from config import CFG

def load_splits(path='dataset_splits.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def prepare_features(data_list, vectorizer=None, mlb=None):
    # 1. Text features
    texts = [item['question'] + " " + item['context'] for item in data_list]
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        x_text = vectorizer.fit_transform(texts)
    else:
        x_text = vectorizer.transform(texts)
    
    # 2. Mesh category features (one-hot)
    # Extract categories for each sample
    mesh_cats_list = []
    for item in data_list:
        cats = set()
        for m in item.get('meshes', []):
            cats.update(m.get('categories', []))
        mesh_cats_list.append(list(cats))
    
    if mlb is None:
        mlb = MultiLabelBinarizer()
        x_mesh = mlb.fit_transform(mesh_cats_list)
    else:
        x_mesh = mlb.transform(mesh_cats_list)
    
    # 3. Combine
    features = hstack([x_text, x_mesh])
    return features, vectorizer, mlb

def run_baseline():
    splits = load_splits()
    test_data = splits['test']
    folds = splits['folds']
    
    val_accuracies = []
    val_f1s = []
    
    print("--- Logistic Regression Baseline (5-Fold CV) ---")
    
    for f in folds:
        fold_idx = f['fold']
        train_data = f['train']
        val_data = f['val']
        
        # Prepare training data
        y_train = [item['final_decision'] for item in train_data]
        x_train, vec, mlb = prepare_features(train_data)
        
        # Train model
        model = LogisticRegression(max_iter=1000, random_state=CFG.SEED, class_weight='balanced')
        model.fit(x_train, y_train)
        
        # Validate
        y_val = [item['final_decision'] for item in val_data]
        x_val, _, _ = prepare_features(val_data, vec, mlb)
        y_pred = model.predict(x_val)
        
        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average='macro')
        
        val_accuracies.append(acc)
        val_f1s.append(f1)
        
        print(f"Fold {fold_idx}: Accuracy={acc:.4f}, Macro F1={f1:.4f}")
    
    print("\n--- CV Results Summary ---")
    print(f"Mean Accuracy: {np.mean(val_accuracies):.4f} (+/- {np.std(val_accuracies):.4f})")
    print(f"Mean Macro F1: {np.mean(val_f1s):.4f} (+/- {np.std(val_f1s):.4f})")
    
    # Final Test Set Evaluation (using the last trained model or re-training on all train+val)
    # For baseline, let's re-train on the full train+val set
    print("\n--- Final Test Set Evaluation ---")
    all_train_val = []
    for f in folds:
        all_train_val.extend(f['val']) # Val sets are non-overlapping and cover the whole train_val set
    
    y_full = [item['final_decision'] for item in all_train_val]
    x_full, final_vec, final_mlb = prepare_features(all_train_val)
    
    final_model = LogisticRegression(max_iter=1000, random_state=CFG.SEED, class_weight='balanced')
    final_model.fit(x_full, y_full)
    
    y_test = [item['final_decision'] for item in test_data]
    x_test, _, _ = prepare_features(test_data, final_vec, final_mlb)
    y_test_pred = final_model.predict(x_test)
    
    test_acc = accuracy_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred, average='macro')
    
    print(classification_report(y_test, y_test_pred))
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Macro F1: {test_f1:.4f}")

if __name__ == "__main__":
    run_baseline()
