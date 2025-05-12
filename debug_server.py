import ollama
import sys
import importlib
import inspect

def debug_ollama():
    print("=== Ollama Package Debug ===")
    
    # Check package information
    print(f"\n1. Python version: {sys.version}")
    print(f"2. Ollama package location: {ollama.__file__}")
    print(f"3. Ollama package version: {getattr(ollama, '__version__', 'Not available')}")
    
    # List available methods in the ollama module
    print("\n4. Available methods in ollama module:")
    methods = [name for name, obj in inspect.getmembers(ollama) 
               if not name.startswith('_') and callable(obj)]
    for method in methods:
        print(f"  - {method}")
    
    # Try the list method
    print("\n5. Attempting ollama.list():")
    try:
        models_response = ollama.list()
        print(f"Type: {type(models_response)}")
        print(f"Content: {models_response}")
        
        # Try to extract model information regardless of format
        print("\n6. Attempting to extract model data:")
        if isinstance(models_response, dict):
            if 'models' in models_response:
                models = models_response['models']
                print(f"Found 'models' key with {len(models)} items")
                print(f"First item sample: {models[0] if models else 'None'}")
            else:
                print(f"Keys in response: {list(models_response.keys())}")
        elif isinstance(models_response, list):
            print(f"Response is a list with {len(models_response)} items")
            print(f"First item sample: {models_response[0] if models_response else 'None'}")
        else:
            print(f"Response is of unexpected type: {type(models_response)}")
            
    except Exception as e:
        print(f"Error calling ollama.list(): {str(e)}")
        print("Stack trace:", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    debug_ollama()
