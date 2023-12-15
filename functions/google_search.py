from typing import ClassVar
from instructor import OpenAISchema
from pydantic import Field
import json
import os
import requests

class GoogleSearch(OpenAISchema):
    """
    This tool performs a search on Google using the serpapi service with an API key sourced from the environment variable 'SERPAPI_API_KEY'.
    It sends a query to the serpapi Google Search API and retrieves the search results. The tool is designed to use 'serpapi.com' as its base URL and
    pass the 'q' parameter for the search query. It sets the location parameter to 'United States' to ensure that the search results are localized
    to that region. The response returned by serpapi is a JSON object, from which the tool extracts the 'organic_results' key. The tool then
    converts the value associated with 'organic_results' into a JSON string and returns it as the output. This is useful for applications needing to
    process or display Google search results from the United States without the overhead of handling the entire API response.
    """
    required_modules: ClassVar = [
        "requests"
    ]

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")
    
    query: str = Field(
        ..., description="The search query to send to the serpapi Google Search API."
    )

    def run(self):
        try:
            api_key = os.getenv('SERPAPI_API_KEY')
            if not api_key:
                raise ValueError("SERPAPI_API_KEY environment variable not set")
            base_url = 'https://serpapi.com/search.json'
            params = {
                'engine': 'google',
                'q': self.query,
                'location': 'United States',
                'api_key': api_key
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            search_results = response.json().get('organic_results')
            return json.dumps(search_results)
        except Exception as e:
            return json.dumps({"error": str(e)})