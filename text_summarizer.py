# Import the tkinter, Ollama, and langchain libraries, along with anything else we might need
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ollama
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

# Set up LLM query
def summarize_text(text):
    """Summarizes text using the local gemma3:12b LLM via Ollama"""
    prompt = (
        "Read the following text and create a summary.\n"
        "First, list the five most important points in the text as bullet points.\n"
        "Then, write a detailed summary paragraph (~250 words).\n\n"
        "Text:\n"
        "{input_text}\n\n"
        "Summary:\n"
        "- "
    )
    template = PromptTemplate(input_variables=["input_text"], template=prompt)
    llm = Ollama(model="gemma3:12b")
    summary = llm(template.format(input_text=text))
    return summary

# Use tkinter to build a simple GUI where a user can upload a text file

# Set up a query to the local gemma3:12b library which asks it to read the text file and create a summary
# The summary should start with five bullet points which are the most important points/elements in the text
# The summary should end with a short paragraph (of ~250 words) which is a more detailed summary of the text

# Finally, the user should be offered the opportunity to save the summary to a local file, again using a simple tkinter GUI