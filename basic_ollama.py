# Basic Ollama implementation

# Import statements
import ollama
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Function to select a local LLM
def select_llm():
    """This function helps the user to select a local LLM available in Ollama."""
    try:
        # Fetch available models in Ollama
        response = ollama.list()
        
        # Extract model names from the ListResponse object
        # In the new API, models is an attribute and each model's name is in the 'model' attribute of each Model object
        model_names = []
        for model in response.models:
            model_names.append(model.model)  # Use .model attribute to get the name
        
        if not model_names:
            print("No models found. Using default model: 'gemma3:12b'")
            return 'gemma3:12b'
        
        # Display available models
        print('Available models:')
        for idx, name in enumerate(model_names, 1):
            print(f'{idx}. {name}')
        
        # Get user selection with validation
        while True:
            try:
                selection = input('Enter the number of the model you want to use: ')
                selection_idx = int(selection) - 1
                
                if 0 <= selection_idx < len(model_names):
                    selected_model = model_names[selection_idx]
                    print(f'Selected model: {selected_model}')
                    return selected_model
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(model_names)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    except Exception as e:
        print(f'Error: {e}')
        print('Make sure your local Ollama server is running. Using default model: "gemma3:12b".')
        return 'gemma3:12b'


# Function to define the "role" of the LLM assistant
def define_role():
    """
    This function allows the user to define the role of the LLM assistant.
    i.e., whether it should act as a teacher, friend, or any other role.
    If the user doesn't want to define a role, it can be set to None or an empty string in the prompt that evtually gets sent to the LLM.
    """
    # Prompt user for role
    print('\nPlease define the role of the LLM assistant.')
    print('Examples: teacher, historian, programmer, friend, etc.')
    print('You may leave this blank if you have no specific role in mind.')
    role = input('Enter role: ')
    
    # If role was defined, print a notification and return the string
    if role.strip():
        print(f'Role defined as: {role}')
        return role
    
    # If no role was defined, print a notification and return None
    else:
        print('No specific role defined. Proceeding without a defined role.')
        return None


# Function to choose a response style - either one of pre-defined options or free-entry
def define_response_style():
    """
    This function allows the user to choose a response style for the LLM assistant.
    User will be offered a pre-defined list of common response styles or can provide their own.
    Initial thoughts for response styles include: concise, detailed, outline-style.
    """
    print('\nSelect a response style:')
    styles = ['Normal', 'Concise', 'Detailed', 'Outline-style', 'Custom']
    
    # Display available styles
    for idx, style in enumerate(styles, 1):
        print(f'{idx}. {style}')
    
    # Prompt user for choice
    choice = int(input('Enter your choice (1-5): '))
    
    # Handle custom response style
    if choice == 4:
        custom_style = input('Enter your custom response style: ').strip()
        return custom_style
    
    else:
        return styles[choice-1]


# Function to provide the actual prompt
def build_prompt():
    """
    This function allows the user to provide the actual prompt for the LLM assistant.
    The prompt can be a simple question or a more complex request.
    """
    print('\nEnter your prompt/question:')
    # Prompt user for input
    user_prompt = input("> ").strip()
    
    return user_prompt


# Function to send the langchain call to the LLM and provide a response
def send_query(model_name, role, style, prompt_text):
    """
    This function sends the query to the LLM and retrieves the response.
    It uses the langchain library to handle the interaction with the LLM.
    """
    # Initialize the Ollama model
    llm = Ollama(model=model_name)
    
    # Build template based on whether role is provided
    if role:
        template = f"""You are a {role}.

Question: {{question}}

Please provide a {style} answer."""
        
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["question"]
        )
    
    else:
        template = f"""Question: {{question}}

Please provide a {style} answer."""
        
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["question"]
        )
    
    # Create the chain
    chain = LLMChain(prompt=prompt_template, llm=llm)
    
    # Get response
    try:
        response = chain.run(question=prompt_text)
        return response
    
    except Exception as e:
        return f'Error getting response: {str(e)}'


def main():
    """Main function to run the program."""
    print('Welcome to the Ollama local LLM Interface.\n')
    
    # Select model
    model_name = select_llm()
    
    # Define role
    role = define_role()
    
    # Define style
    style = define_response_style()
    
    # Build prompt
    prompt_text = build_prompt()
    
    # Send query and print response
    print('\nSending query to LLM, please wait...\n')
    response = send_query(model_name, role, style, prompt_text)
    
    print('\n=== LLM Response ===\n')
    print(response)

if __name__ == '__main__':
    main()
