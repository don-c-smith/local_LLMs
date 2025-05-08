# Basic Ollama implementation

# Import statements
import ollama
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Function to select a local LLM
def select_llm():
    """This function helps the user to select a local LLM available in Ollama."""
    # Fetch available models in Ollama
    try:
        models = ollama.list()
        model_names = [model['name'] for model in models['models']]
        
        # Display available models
        print('Available models:')
        for idx, name in enumerate(model_names, 1):
            print(f'{idx}. {name}')
        
        # Get user selection
        selection = int(input('Enter the number of the model you want to use: '))
        selected_model = model_names[selection-1]
        print(f'Selected model: {selected_model}')
        return selected_model
    
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
    print('Please define the role of the LLM assistant.')
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


# Function to provide the actual prompt
def build_prompt():
    """
    This function allows the user to provide the actual prompt for the LLM assistant.
    The prompt can be a simple question or a more complex request.
    """

# Function to send the langchain call to the LLM and provide a response
def send_query():
    """
    This function sends the query to the LLM and retrieves the response.
    It uses the langchain library to handle the interaction with the LLM.
    """
    