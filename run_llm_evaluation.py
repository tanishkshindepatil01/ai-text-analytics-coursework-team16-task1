import os
import sys
from batch_process import batch_process
from evaluate_llm import run_evaluation

def main():
    input_file = "dataset_splits.json"
    output_file = "results_llm_test.json"
    split_key = "test"
    
    # 1. Run Batch Processing (with breakpoint support)
    print("Step 1: Running LLM Batch Processing...")
    # You can set limit=5 for a quick test run
    limit = None 
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        limit = 5
        print("Running in test mode with limit=5")
        
    batch_process(
        input_file=input_file, 
        output_file=output_file, 
        split_key=split_key, 
        limit=limit
    )
    
    # 2. Run Evaluation
    print("\nStep 2: Running Evaluation...")
    run_evaluation(output_file)

if __name__ == "__main__":
    main()
