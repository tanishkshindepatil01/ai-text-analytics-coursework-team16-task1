import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiDecisionMaker:
    """
    A class to use Google Gemini API for making decisions on medical questions
    based on provided contexts, with structured JSON output.
    """
    
    def __init__(self, model_name="gemini-3.1-flash-lite-preview"):
        """
        Initialize the Gemini API client.
        
        Args:
            model_name (str): The name of the Gemini model to use.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")
        
        genai.configure(api_key=api_key)
        
        # Define the JSON schema for the response
        self.response_schema = {
            "type": "object",
            "properties": {
                "final_decision": {
                    "type": "string",
                    "description": "The final decision based on the context. Must be one of 'yes', 'no', or 'maybe'.",
                    "enum": ["yes", "no", "maybe"]
                }
            },
            "required": ["final_decision"]
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": self.response_schema,
                "temperature": 0.1,  # Lower temperature for more deterministic results
            }
        )

    def predict(self, question, contexts):
        """
        Predict the final decision for a given question and its contexts.
        
        Args:
            question (str): The medical question.
            contexts (list or str): A list of context strings or a single context string.
            
        Returns:
            dict: A dictionary containing 'final_decision'.
        """
        # Prepare the context text
        if isinstance(contexts, list):
            context_text = "\n\n".join(contexts)
        else:
            context_text = contexts
            
        # Construct the prompt
        prompt = (
            f"You are a medical expert assistant. Based on the provided contexts, "
            f"answer the question with 'yes', 'no', or 'maybe'.\n\n"
            f"Question: {question}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Provide your answer in the specified JSON format."
        )
        
        try:
            response = self.model.generate_content(prompt)
            # Parse the JSON response
            return json.loads(response.text)
        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            return {
                "final_decision": "error"
            }

if __name__ == "__main__":
    # Quick test if run directly
    try:
        maker = GeminiDecisionMaker()
        sample_q = "Do mitochondria play a role in remodelling lace plant leaves during programmed cell death?"
        sample_c = [
            "Programmed cell death (PCD) is the regulated death of cells within an organism...",
            "The following paper elucidates the role of mitochondrial dynamics during developmentally regulated PCD..."
        ]
        result = maker.predict(sample_q, sample_c)
        print("Test Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Setup error: {e}")
