# Import the tkinter, Ollama, and langchain libraries, along with anything else we might need
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox  # Additional tkinter components
from langchain_ollama import OllamaLLM  # New modern import for Ollama
from langchain.prompts import PromptTemplate  # For structured prompt formatting

# Set up LLM query function to process text with the local LLM
def summarize_text(text):
    """Summarizes text using the local gemma3:12b LLM via Ollama
    
    Args:
        text (str): The input text to be summarized
        
    Returns:
        str: The generated summary from the LLM
    """
    # Define a detailed prompt template that instructs the LLM how to format the summary
    prompt = (
        "Read the following text and create a summary.\n"
        "First, list the five most important points in the text as bullet points.\n"
        "Then, write a more detailed summary paragraph (~250 words).\n\n"
        "Text:\n"
        "{input_text}\n\n"
        "Summary:\n"
        "- "  # Starting with a bullet point to guide the format
    )
    # Create a LangChain prompt template with the input variable
    template = PromptTemplate(input_variables=["input_text"], template=prompt)
    
    # Initialize the Ollama LLM with the specified model - using modern OllamaLLM
    llm = OllamaLLM(model="gemma3:12b")
    
    # Generate the summary by sending the formatted prompt to the LLM
    formatted_prompt = template.format(input_text=text)
    summary = llm.invoke(formatted_prompt)
    
    return summary

# Main function to build and manage the GUI application
def create_gui():
    """Creates and configures the main GUI window with all necessary components"""
    # Set up the main application window
    window = tk.Tk()
    window.title("Text Summarizer")
    window.geometry("800x600")  # Set initial window size
    
    # Variable to store the content of the loaded file
    file_content = ""
    
    # Function to handle file upload via dialog
    def upload_file():
        """Opens file dialog and loads selected text file into the input area"""
        # Open file dialog with filter for text files
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return  # User canceled the dialog
            
        # Read the selected file's content
        with open(file_path, "r", encoding="utf-8") as file:
            nonlocal file_content  # Use the outer function's variable
            file_content = file.read()
            
        # Display the file content in the input text area
        input_text.delete(1.0, tk.END)  # Clear existing content
        input_text.insert(tk.END, file_content)  # Insert new content
        status_label.config(text=f"Loaded: {file_path}")  # Update status bar
        summarize_btn.config(state=tk.NORMAL)  # Enable the summarize button now that we have content
    
    # Function to process the text and generate a summary
    def process_text():
        """Sends the loaded text to the LLM for summarization"""
        # Check if there's any text to process
        if not file_content.strip():
            messagebox.showwarning("Warning", "No text to summarize")
            return
            
        # Update status to show processing is happening
        status_label.config(text="Generating summary... Please wait")
        window.update()  # Force UI update to show the status change
        
        # Try to generate the summary, handling any errors
        try:
            # Call the LLM function to summarize the text
            summary = summarize_text(file_content)
            
            # Display the generated summary in the output area
            output_text.delete(1.0, tk.END)  # Clear existing output
            output_text.insert(tk.END, summary)  # Insert the summary
            save_btn.config(state=tk.NORMAL)  # Enable the save button
            status_label.config(text="Summary complete")  # Update status
        except Exception as e:
            # Handle any errors during summarization
            messagebox.showerror("Error", f"Failed to generate summary: {e}")
            status_label.config(text="Error occurred")
    
    # Function to save the generated summary to a file
    def save_summary():
        """Saves the generated summary to a user-specified text file"""
        # Get the current summary text from the output area
        summary = output_text.get(1.0, tk.END)
        
        # Check if there's a summary to save
        if not summary.strip():
            messagebox.showwarning("Warning", "No summary to save")
            return
            
        # Open save dialog to get destination path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Default to .txt extension
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]  # File type options
        )
        
        # Save the summary if a path was selected
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(summary)
            status_label.config(text=f"Summary saved to: {file_path}")  # Update status
    
    # Create and configure UI components
    # Main frame to hold all components
    frame = tk.Frame(window, padx=10, pady=10)  # Add padding around edges
    frame.pack(fill=tk.BOTH, expand=True)  # Fill the entire window
    
    # Frame for the input text area with a label
    input_frame = tk.LabelFrame(frame, text="Input Text")
    input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Scrollable text area for input text
    input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD)  # Word wrap enabled
    input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Frame to hold the action buttons
    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=5)  # Stretch horizontally
    
    # Button to open the file upload dialog
    upload_btn = tk.Button(btn_frame, text="Upload Text File", command=upload_file)
    upload_btn.pack(side=tk.LEFT, padx=5)
    
    # Button to trigger summarization (initially disabled until file is loaded)
    summarize_btn = tk.Button(btn_frame, text="Summarize", command=process_text, state=tk.DISABLED)
    summarize_btn.pack(side=tk.LEFT, padx=5)
    
    # Frame for the summary output area with a label
    output_frame = tk.LabelFrame(frame, text="Summary")
    output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Scrollable text area for the generated summary
    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)  # Word wrap enabled
    output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Button to save the summary (initially disabled until summary is generated)
    save_btn = tk.Button(frame, text="Save Summary", command=save_summary, state=tk.DISABLED)
    save_btn.pack(pady=5)
    
    # Label at the bottom of the window to show application status
    status_label = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)  # Placed at bottom, full width
    
    return window

# Entry point for the application
# The application will run until the user closes the window
if __name__ == "__main__":
    app = create_gui()  # Create the GUI
    app.mainloop()  # Start the tkinter event loop
    