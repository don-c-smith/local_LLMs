# Basic Ollama implementation

# Import statements - Ollama, langchain, etc

# Function to select a local LLM
def select_llm():
    """This function helps the user to select a local LLM available in Ollama."""

# Function to define the "role" of the LLM assistant
def define_role():
    """
    This function allows the user to define the role of the LLM assistant.
    i.e., whether it should act as a teacher, friend, or any other role.
    If the user doesn't want to define a role, it can be set to None or an empty string in the prompt that evtually gets sent to the LLM.
    """

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
    