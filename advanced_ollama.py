# Import statements
import os
import sys
import time
import signal
import ollama
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import textwrap

# Constants
DEFAULT_MODEL = 'gemma3:12b'
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
MAX_PROMPT_LENGTH = 4000
WRAPPER = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print('\nExiting the program. Goodbye!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Function to select a local LLM
def select_llm(retries=0):
    """This function helps the user to select a local LLM available in Ollama."""
    if retries >= MAX_RETRIES:
        print(f'Failed to connect to Ollama after {MAX_RETRIES} attempts.')
        print(f'Using default model: "{DEFAULT_MODEL}" (if Ollama starts working)')
        return DEFAULT_MODEL
    
    try:
        # Fetch available models in Ollama
        response = ollama.list()
        
        # Extract model names from the ListResponse object
        model_names = []
        for model in response.models:
            model_names.append(model.model)  # Use .model attribute to fetch the name
        
        if not model_names:
            print('No local models were found in your Ollama installation.')
            install_choice = input('Would you like to install the default model? (Y/N): ').lower()
            
            if install_choice.startswith('y'):
                print(f'Please run "ollama pull {DEFAULT_MODEL}" in your terminal.')
            
            print(f'Using default model: "{DEFAULT_MODEL}"')
            return DEFAULT_MODEL
        
        # Check for environment variable to skip selection
        env_model = os.environ.get('OLLAMA_DEFAULT_MODEL')
        if env_model and env_model in model_names:
            print(f'Using model from environment variable: "{env_model}"')
            return env_model
        
        # Display available models
        print('Available models:')
        for idx, name in enumerate(model_names, 1):
            print(f'{idx}. {name}')
        
        # Get user selection with validation
        while True:
            try:
                selection = input('Enter the number of the model you want to use (or press Enter to use the default model): ')
                
                # Handle empty input (default)
                if not selection.strip():
                    # If DEFAULT_MODEL is available, use it; otherwise use first available model
                    if DEFAULT_MODEL in model_names:
                        print(f'Using default model: "{DEFAULT_MODEL}"')
                        return DEFAULT_MODEL
                    else:
                        print(f'Using first available model: "{model_names[0]}"')
                        return model_names[0]
                
                selection_idx = int(selection) - 1
                
                if 0 <= selection_idx < len(model_names):
                    selected_model = model_names[selection_idx]
                    print(f'Selected model: {selected_model}')
                    return selected_model
                else:
                    print(f'Invalid selection. Please enter a number between 1 and {len(model_names)}.')
            except ValueError:
                print('Please enter a valid number or press Enter to use the default model.')
    
    except ConnectionRefusedError:
        print('Error: Could not connect to Ollama server.')
        print('Make sure the Ollama server is running (run "ollama serve" in your terminal).')
        retry = input(f'Retry connection? (Y/N, {MAX_RETRIES-retries} attempts left): ').lower()
        if retry.startswith('y'):
            print(f'Retrying in {RETRY_DELAY} seconds...')
            time.sleep(RETRY_DELAY)
            return select_llm(retries + 1)
        
        else:
            print(f'Using default model: "{DEFAULT_MODEL}" (if Ollama starts working)')
            return DEFAULT_MODEL
    
    except Exception as e:
        print(f'Error connecting to Ollama: {e}')
        print(f'Make sure your local Ollama server is running. Using default model: "{DEFAULT_MODEL}"')
        return DEFAULT_MODEL


# Function to define the "role" of the LLM assistant
def define_role():
    """
    This function allows the user to define the role of the LLM assistant.
    """
    # Predefined roles for quick selection
    roles = ['Teacher', 'Programmer', 'Historian', 'Scientist', 'Writing assistant', 'Creative writer', 'Business consultant']
    
    print('\nPlease define the role of the LLM assistant.')
    print('Examples: teacher, historian, programmer, friend, etc.')
    print('Common roles:')
    for idx, role in enumerate(roles, 1):
        print(f'{idx}. {role}')
    print('0. Custom role')
    print('Press Enter to skip this step (i.e. to assign no specific role to the model)')
    
    while True:
        role_input = input('Select number or enter a custom role: ')
        
        # Handle empty input
        if not role_input.strip():
            print('No specific role defined. Proceeding without a defined role.')
            return None
        
        # Handle numeric selection
        try:
            selection = int(role_input)
            if selection == 0:
                custom_role = input('Enter your custom role: ').strip()
                if custom_role:
                    if len(custom_role) > 50:
                        print('Role description too long. Please keep your description under 50 characters.')
                        continue
                    print(f'Role defined as: {custom_role}')
                    return custom_role
                
                else:
                    print('No specific role entered. Proceeding without a defined role.')
                    return None
            
            elif 1 <= selection <= len(roles):
                selected_role = roles[selection-1]
                print(f'Role defined as: {selected_role}')
                return selected_role
            
            else:
                print(f'Invalid selection. Please enter a number between 0 and {len(roles)}.')
        
        # Handle text input (custom role)
        except ValueError:
            if len(role_input) > 50:
                print('Role description too long. Please keep your description under 50 characters.')
                continue
            print(f'Role defined as: {role_input}')
            return role_input


# Function to choose a response style
def define_response_style():
    """
    This function allows the user to choose a response style for the LLM assistant.
    """
    # Dictionary of styles with descriptions
    styles = {
        'Normal': 'Standard, balanced response',
        'Concise': 'Brief and to the point',
        'Detailed': 'Thorough and comprehensive',
        'Outline-style': 'Organized with headings and bullet points',
        'ELI5': 'Explained as if to a 5-year-old',
        'Custom': 'Define your own style'
    }
    
    print('\nSelect a response style:')
    
    # Display available styles
    for idx, (style, description) in enumerate(styles.items(), 1):
        print(f'{idx}. {style} - {description}')
    
    # Get user selection with validation
    while True:
        try:
            selection = input('Enter the number of the response style (or press Enter for Normal): ')
            
            # Handle empty input (default)
            if not selection.strip():
                print('Selected response style: Normal')
                return 'Normal'
            
            selection_idx = int(selection)
            
            if 1 <= selection_idx <= len(styles):
                selected_style = list(styles.keys())[selection_idx-1]
                
                # Handle custom response style
                if selected_style == 'Custom':
                    while True:
                        custom_style = input('Enter your custom response style: ').strip()
                        if not custom_style:
                            print('Empty style. Using Normal instead.')
                            return 'Normal'
                        elif len(custom_style) > 100:
                            print('Style description too long. Please keep it under 100 characters.')
                        else:
                            print(f'Defined response style as: {custom_style}')
                            return custom_style
                else:
                    print(f'Selected response style: {selected_style}')
                    return selected_style
            
            else:
                print(f'Invalid selection. Please enter a number between 1 and {len(styles)}.')
        
        except ValueError:
            print('Invalid selection. Please enter a valid number or press Enter for default.')


# Function to provide the actual prompt
def build_prompt():
    """
    This function allows the user to provide the actual prompt for the LLM assistant.
    Supports multiline input and basic validation.
    """
    print('\nEnter your prompt/question (type "END" on a new line when finished):')
    print('For a single line prompt, just type your question and press Enter.')
    
    lines = []
    first_line = input(">>> ").strip()
    
    # Check if we need multiline input
    if first_line.lower() == "end":
        print("Empty prompt. Please enter a valid prompt.")
        return build_prompt()
    elif "\\n" in first_line:
        # Handle escaped newlines
        prompt = first_line.replace("\\n", "\n")
        print("\nPrompt received with line breaks.")
    else:
        lines.append(first_line)
        
        # Check if we need more lines
        line = input("... ").strip()
        while line.lower() != "end" and line:
            lines.append(line)
            line = input("... ").strip()
        
        prompt = "\n".join(lines)
    
    # Validate prompt
    if not prompt.strip():
        print("Empty prompt. Please enter a valid prompt.")
        return build_prompt()
    
    if len(prompt) > MAX_PROMPT_LENGTH:
        print(f"Warning: Your prompt is very long ({len(prompt)} characters). This may affect performance.")
        confirm = input("Continue with this prompt? (y/n): ").lower()
        if not confirm.startswith('y'):
            return build_prompt()
    
    # Preview the prompt
    print("\nYour prompt:")
    for line in WRAPPER.wrap(prompt):
        print(f"> {line}")
    
    # Confirm prompt
    confirm = input("\nIs this correct? (y/n): ").lower()
    if confirm.startswith('y'):
        return prompt
    else:
        return build_prompt()


# Function to send the langchain call to the LLM and provide a response
def send_query(model_name, role, style, prompt_text):
    """
    This function sends the query to the LLM and retrieves the response.
    Added error handling, timeout control, and progress indication.
    """
    print('\nSending query to LLM, please wait...')
    start_time = time.time()
    
    try:
        # Show a simple progress indicator
        progress_thread = None
        try:
            from threading import Thread
            
            def show_progress():
                chars = ["-", "\\", "|", "/"]
                i = 0
                while True:
                    sys.stdout.write(f"\rProcessing {chars[i]} ")
                    sys.stdout.flush()
                    i = (i + 1) % len(chars)
                    time.sleep(0.2)
                    if time.time() - start_time > 120:  # 2 minute timeout
                        sys.stdout.write("\rProcessing is taking longer than expected... ")
                        sys.stdout.flush()
            
            progress_thread = Thread(target=show_progress)
            progress_thread.daemon = True
            progress_thread.start()
        except ImportError:
            pass
        
        # Import the correct class
        try:
            from langchain_ollama import OllamaLLM
        except ImportError:
            print("Warning: langchain_ollama package not found. Falling back to legacy implementation.")
            OllamaLLM = Ollama
        
        # Initialize the Ollama model
        try:
            llm = OllamaLLM(model=model_name)
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            print(f"Falling back to default model: '{DEFAULT_MODEL}'")
            llm = OllamaLLM(model=DEFAULT_MODEL)
        
        # Handle "Normal" style by making it empty
        style_instruction = f"Please provide a {style} answer." if style.lower() != "normal" else ""
        
        # Build template based on whether role is provided
        if role:
            template = f"""You are a {role}.

Question: {{question}}

{style_instruction}"""
        else:
            template = f"""Question: {{question}}

{style_instruction}"""
        
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["question"]
        )
        
        # Try using modern pipe syntax, but fall back to old chain method if needed
        try:
            chain = prompt_template | llm
            response = chain.invoke({"question": prompt_text})
        except (AttributeError, TypeError):
            # Fall back to LLMChain method for older versions
            from langchain.chains import LLMChain
            chain = LLMChain(llm=llm, prompt=prompt_template)
            response = chain.run(question=prompt_text)
        
        # Stop progress indicator if it's running
        if progress_thread:
            sys.stdout.write("\r" + " " * 30 + "\r")  # Clear the progress line
            sys.stdout.flush()
        
        elapsed_time = time.time() - start_time
        print(f"Response received in {elapsed_time:.2f} seconds.")
        
        return response
    
    except Exception as e:
        # Stop progress indicator if it's running
        if 'progress_thread' in locals() and progress_thread:
            sys.stdout.write("\r" + " " * 30 + "\r")  # Clear the progress line
            sys.stdout.flush()
        
        error_msg = str(e)
        if "connection refused" in error_msg.lower():
            return "Error: Could not connect to Ollama server. Please make sure it's running by executing 'ollama serve' in a terminal."
        elif "not found" in error_msg.lower() and model_name in error_msg:
            return f"Error: Model '{model_name}' not found. You may need to download it first with 'ollama pull {model_name}'."
        elif "timeout" in error_msg.lower():
            return "Error: The request timed out. The model might be too large for your system or Ollama might be busy."
        else:
            return f'Error getting response: {error_msg}\n\nPlease check if Ollama is running correctly.'


def save_conversation(prompt, response, model, role, style):
    """
    Offers to save the conversation to a file.
    """
    save = input("\nWould you like to save this conversation? (y/n): ").lower()
    if not save.startswith('y'):
        return
    
    filename = input("Enter filename (default: ollama_conversation.txt): ").strip()
    if not filename:
        filename = "ollama_conversation.txt"
    
    mode = 'a' if os.path.exists(filename) else 'w'
    
    try:
        with open(filename, mode) as f:
            f.write(f"{'=' * 80}\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {model}\n")
            if role:
                f.write(f"Role: {role}\n")
            f.write(f"Style: {style}\n")
            f.write(f"\nPROMPT:\n{prompt}\n\n")
            f.write(f"RESPONSE:\n{response}\n\n")
        print(f"Conversation saved to {filename}")
    except Exception as e:
        print(f"Error saving conversation: {e}")


def main():
    """Main function to run the program with basic conversation loop."""
    print('Welcome to the Ollama local LLM Interface.\n')
    print('Press Ctrl+C at any time to exit the program.\n')
    
    try:
        # Select model
        model_name = select_llm()
        
        # Define role
        role = define_role()
        
        # Define style
        style = define_response_style()
        
        # Conversation loop
        while True:
            # Build prompt
            prompt_text = build_prompt()
            
            # Send query and print response
            response = send_query(model_name, role, style, prompt_text)
            
            print('\n=== LLM Response ===\n')
            print(response)
            print('\n=== End Response ===\n')
            
            # Offer to save the conversation
            save_conversation(prompt_text, response, model_name, role, style)
            
            # Ask if the user wants to continue
            continue_chat = input("\nAsk another question? (y/n): ").lower()
            if not continue_chat.startswith('y'):
                print("\nThank you for using the Ollama LLM Interface. Goodbye!")
                break
            
            # Ask if user wants to change settings
            change_settings = input("Change model, role, or style? (y/n): ").lower()
            if change_settings.startswith('y'):
                change_what = input("What would you like to change? (model/role/style/all): ").lower()
                
                if 'model' in change_what or 'all' in change_what:
                    model_name = select_llm()
                
                if 'role' in change_what or 'all' in change_what:
                    role = define_role()
                
                if 'style' in change_what or 'all' in change_what:
                    style = define_response_style()
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Exiting the program.")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())