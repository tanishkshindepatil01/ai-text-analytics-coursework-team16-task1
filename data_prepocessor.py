import os
import re
import json
from typing import Dict, List

class DataPreprocessor:
    def __init__(self):
        self.label2id = {"no": 0, "maybe": 1, "yes": 2}
        self.id2label = {0: "no", 1: "maybe", 2: "yes"}

    def clean_text(self, text: str) -> str:
        """Text cleaning logic from reference notebook."""
        text = str(text).lower()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s\-\?\.,:;/%()]", " ", text)
        return text.strip()

    def get_handcrafted_features(self, question_clean: str, context_clean: str) -> Dict[str, int]:
        """Binary features from reference notebook."""
        features = {}
        
        # Question-based features
        features["has_negation"] = int(any(w in question_clean.split() for w in ["no", "not", "without", "lack", "absence"]))
        features["has_causal"] = int(any(w in question_clean for w in ["cause", "effect", "impact", "influence", "affect", "lead to"]))
        features["has_comparison"] = int(any(w in question_clean for w in ["compar", "differ", "versus", "vs", "better", "worse"]))
        features["has_association"] = int(any(w in question_clean for w in ["associat", "correlat", "relat", "link"]))
        features["has_risk"] = int("risk" in question_clean)
        
        # Context-based features
        features["context_evidence_strength"] = int(any(w in context_clean for w in ["significant", "strongly", "clearly", "demonstrated"]))
        features["context_hedging"] = int(any(w in context_clean for w in ["may", "might", "suggest", "possibly", "further study", "inconclusive"]))
        
        return features

    def process_data(self, data: Dict) -> List[Dict]:
        """
        Processes raw PubMedQA data into the format used in the reference notebook.
        """
        processed_data = []
        for pmid, item in data.items():
            # Extract raw fields
            question = item.get('QUESTION', '')
            contexts = item.get('CONTEXTS', [])
            context = " ".join(contexts) if isinstance(contexts, list) else str(contexts)
            long_answer = item.get('LONG_ANSWER', '')
            label = str(item.get('final_decision', '')).lower().strip()
            
            # 1. Clean text
            q_clean = self.clean_text(question)
            c_clean = self.clean_text(context)
            a_clean = self.clean_text(long_answer)
            
            # 2. Text variants
            text_q_only = f"question: {q_clean}"
            text_q_ctx = f"question: {q_clean} context: {c_clean}"
            text_q_ctx_ans = f"question: {q_clean} context: {c_clean} answer: {a_clean}"
            
            q_only = q_clean
            q_ctx = f"{q_clean} [SEP] {c_clean}"
            q_ctx_ans = f"{q_clean} [SEP] {c_clean} [SEP] {a_clean}"
            
            # 3. Handcrafted features
            handcrafted = self.get_handcrafted_features(q_clean, c_clean)
            
            # 4. Length stats
            q_len = len(q_clean.split())
            c_len = len(c_clean.split())
            a_len = len(a_clean.split())
            num_ctx = len(contexts) if isinstance(contexts, list) else 1
            
            # Combine into record
            record = {
                'pmid': pmid,
                'question': question,
                'context': context,
                'long_answer': long_answer,
                'label': label,
                'label_id': self.label2id.get(label, -1),
                'question_clean': q_clean,
                'context_clean': c_clean,
                'long_answer_clean': a_clean,
                'text_q_only': text_q_only,
                'text_q_ctx': text_q_ctx,
                'text_q_ctx_ans': text_q_ctx_ans,
                'q_only': q_only,
                'q_ctx': q_ctx,
                'q_ctx_ans': q_ctx_ans,
                'question_len': q_len,
                'context_len': c_len,
                'long_answer_len': a_len,
                'num_contexts': num_ctx,
                'final_decision': label # keeping for compatibility
            }
            record.update(handcrafted)
            
            processed_data.append(record)
            
        return processed_data

    def save_processed_data(self, processed_data: List[Dict], output_path: str):
        """Saves the processed data to a JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=4)
        print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # Example usage / standalone run
    DATA_PATH = "ori_pqal.json"
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        processor = DataPreprocessor()
        processed = processor.process_data(raw_data)
        processor.save_processed_data(processed, "processed_pubmedqa.json")
