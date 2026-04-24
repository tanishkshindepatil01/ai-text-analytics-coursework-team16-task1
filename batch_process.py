import json
import os
import time
from modeling_llm_api import GeminiDecisionMaker

def batch_process(input_file="dataset_splits.json", output_file="results_llm_test.json", split_key="test", limit=None):
    """
    Process the PubMedQA dataset in batches with breakpoint continuation support.
    Supports both raw processed files (list) and split files (dict with 'test' key).
    """
    
    # 1. Load input data
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    try:
        with open(input_file, "r") as f:
            raw_data = json.load(f)
            
        # Handle different structures
        if isinstance(raw_data, dict) and split_key in raw_data:
            data = raw_data[split_key]
            print(f"Loaded {len(data)} items from split '{split_key}' in {input_file}.")
        elif isinstance(raw_data, list):
            data = raw_data
            print(f"Loaded {len(data)} items from list in {input_file}.")
        else:
            print(f"Error: Unexpected data structure in {input_file}.")
            return
    except Exception as e:
        print(f"Error loading {input_file}: {e}")
        return
        
    if limit:
        data = data[:limit]

    # 2. Check for existing progress (Breakpoint support)
    processed_results = []
    processed_pmids = set()
    
    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                processed_results = json.load(f)
                processed_pmids = {item["pmid"] for item in processed_results}
                print(f"Resuming from breakpoint. Already processed {len(processed_pmids)} items.")
        except (json.JSONDecodeError, KeyError):
            print(f"Warning: Could not parse {output_file}. Starting fresh.")
            processed_results = []
            processed_pmids = set()

    # 3. Initialize Gemini
    print("Initializing Gemini API...")
    try:
        maker = GeminiDecisionMaker()
    except Exception as e:
        print(f"Initialization error: {e}")
        return

    # 4. Process items
    remaining_data = [item for item in data if item["pmid"] not in processed_pmids]
    print(f"Starting processing. Total remaining items to process: {len(remaining_data)}")
    
    if not remaining_data:
        print("Everything has already been processed!")
        return

    try:
        for i, item in enumerate(remaining_data):
            pmid = item["pmid"]
            question = item["question"]
            context = item["context"]
            
            curr_count = len(processed_results) + 1
            total_count = len(processed_results) + len(remaining_data)
            print(f"[{curr_count}/{total_count}] Processing PMID: {pmid}...")
            
            # Call API
            result = maker.predict(question, context)
            
            # Combine with original metadata
            output_item = {
                "pmid": pmid,
                "question": question,
                "prediction": result.get("final_decision"),
                "ground_truth": item.get("final_decision")
            }
            
            processed_results.append(output_item)
            processed_pmids.add(pmid)
            
            # 5. Save after each successful item
            with open(output_file, "w") as f:
                json.dump(processed_results, f, indent=2)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Progress saved.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print(f"\nProcessing finished. Total results saved in {output_file}: {len(processed_results)}")

if __name__ == "__main__":
    # To process the full test set, set limit=None
    # Defaulting to dataset_splits.json['test']
    batch_process(input_file="dataset_splits.json", output_file="results_llm_test.json", split_key="test", limit=None)
