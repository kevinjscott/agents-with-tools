from typing import ClassVar, List
from instructor import OpenAISchema
from pydantic import Field
import requests

class RetrieveWebFile(OpenAISchema):
    """
    This tool is designed to retrieve files from the web, with a primary focus on robots.txt files. It can be extended to fetch any file by specifying the file path. The tool takes a base URL and a file path as input, performs an HTTP GET request to the composed URL, and returns the content of the file along with the HTTP status code.

    Pros:
    - Easy to use for fetching web files.
    - Extensible to any file path.
    
    Cons:
    - Does not handle complex web scraping scenarios.
    
    Use an alternative tool like BeautifulSoup or Scrapy for more complex web scraping tasks that require parsing HTML or handling JavaScript.
    """
    required_modules: ClassVar[List[str]] = ['requests']

    chain_of_thought: str = Field(
        ..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task."
    )

    base_url: str = Field(
        ..., description="The base URL from which to retrieve the file."
    )
    file_path: str = Field(
        default="robots.txt", description="The file path to retrieve, defaulting to 'robots.txt'."
    )

    def run(self):
        try:
            # Compose the full URL by combining the base URL and file path
            target_url = self.base_url.rstrip('/') + '/' + self.file_path.lstrip('/')
            # Perform the HTTP GET request
            response = requests.get(target_url)
            # Return the HTTP status code and the content of the file
            return f"Status Code: {response.status_code}, Content: {response.text}"
        except Exception as e:
            # Return a useful error message
            return f"Error: {e}"

# Note: No usage information is included in the code as per the instructions.
# The AI will learn how to use the tool from the description provided above.