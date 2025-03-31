
# Required Packages
import ollama

class LLMClient:
    def __init__(self, model_name='llama3'):
        self.model_name = model_name
        print(f"[LLMClient] Initialized with model: {self.model_name}")

    def set_model(self, model_name):
        self.model_name = model_name
        print(f"[LLMClient] Switched to model: {self.model_name}")

    def get_response(self, prompt):
        print(f"[LLMClient] Using model: {self.model_name}")
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
