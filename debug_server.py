import ollama
import json

def debug_ollama():
    print("=== Ollama API Debug ===")
    
    # Check if Ollama server is running
    try:
        # Get version info
        print("\n1. Checking Ollama version:")
        version = ollama.version()
        print(f"Version info: {version}")
        
        # Get raw list response
        print("\n2. Raw response from ollama.list():")
        models_response = ollama.list()
        print(f"Type: {type(models_response)}")
        print(f"Raw content: {models_response}")
        
        # Try to pretty print if it's a dictionary
        if isinstance(models_response, dict):
            print("\n3. Pretty printed response:")
            print(json.dumps(models_response, indent=2))
        
        # Try different ways to access model names
        print("\n4. Attempting to extract model names:")
        
        # Method 1: If response is {'models': [{...}, {...}]}
        if isinstance(models_response, dict) and 'models' in models_response:
            print("Method 1 (models_response['models']):")
            for model in models_response['models']:
                if 'name' in model:
                    print(f"  - {model['name']}")
                else:
                    print(f"  Model object doesn't have 'name' key: {model}")
        
        # Method 2: If response is directly the list of models
        if isinstance(models_response, list):
            print("Method 2 (models_response as list):")
            for model in models_response:
                if isinstance(model, dict) and 'name' in model:
                    print(f"  - {model['name']}")
                elif isinstance(model, str):
                    print(f"  - {model}")
                else:
                    print(f"  Unknown model format: {model}")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure your Ollama server is running.")
