import os
from crewai_tools import BaseTool, SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

# Initialize the web search tool
search_tool = SerperDevTool()

class DocumentReadTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads a financial document from a specified file path and returns its content."

    def _run(self, file_path: str) -> str:
        """
        Reads a PDF document from the given file path and extracts its text content.
        """
        if not os.path.exists(file_path):
            return "Error: The specified file path does not exist."
        
        try:
            # Load the PDF document
            loader = PyPDFLoader(file_path=file_path)
            docs = loader.load_and_split()
            
            # Combine the content of all pages
            full_content = "".join(data.page_content for data in docs)
            return full_content
        except Exception as e:
            return f"Error: An exception occurred while reading the document: {e}"

# Instantiate the document reading tool for agents to use
read_document_tool = DocumentReadTool()