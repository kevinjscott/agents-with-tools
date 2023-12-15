from typing import ClassVar
from instructor import OpenAISchema
from pydantic import Field

class RetrieveToolFileContents(OpenAISchema):
    """
    This tool searches for and retrieves the contents of a Python file with a given name within the 'functions' directory or a first-level subdirectory inside the 'functions' directory.
    
    The tool expects the name of the file to follow the snake_case naming convention i.e. by converting the tool name from TitleCase to snake_case. If the file is not found in the 'functions' directory, a search is done within the first-level subdirectories. 
    
    IMPORTANT: Do not specify an assistant_id parameter.

    Pros:
    - It automates the process of file content retrieval for Python files based on naming conventions.
    - It handles the search within both the main directory and nested subdirectories.
    
    Cons:
    - It is limited to searching within a predefined directory structure and naming convention.
    - It only supports Python files.
    
    If the file structure is unknown or the naming conventions differ, adjustments to the code may be necessary.
    """

    chain_of_thought: str = Field(
        ..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task."
    )
    filename: str = Field(
        ..., description="The snake_case name of the python tool for which the file content is requested (including file extension)."
    )

    def run(self):
        import os
        import glob

        # Start by searching in the 'functions' directory
        file_path = f'functions/{self.filename}'
        if not os.path.isfile(file_path):
            # If not in 'functions', search in first-level subdirectories
            found_files = glob.glob(f'functions/*/{self.filename}')
            if not found_files:
                # If no file is found, explain why
                return f'No file found for {self.filename} in functions or its subdirectories.'
            file_path = found_files[0]
        
        # Read and return the file contents
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
