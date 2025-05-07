# Basic Ollama implementation

# Import statements - Ollama, langchain, etc

# Function to select a local LLM
def select_llm():
    """This function helps the user to select a local LLM available in Ollama."""

# Function to define the "role" of the LLM assistant
def define_role():
    """This function allows the user to define the role of the LLM assistant."""

# Function to choose a response style - either one of pre-defined options or free-entry
def define_response_style():
    """
    This function allows the user to choose a response style for the LLM assistant.
    User will be offered a pre-defined list of common response styles or can provide their own.
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
    