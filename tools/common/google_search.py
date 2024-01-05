from typing import ClassVar, List
from instructor import OpenAISchema
from pydantic import Field
import json
import os
from serpapi import GoogleSearch as serpapi

class GoogleSearch(OpenAISchema):
    """
    This tool searches web content with Google. Google searches never return realtime information, so if you're looking for the most up-to-date content, you'll need to scrape it directly from a website. That said you could use a Google search to find the url of a website and then go crawl it.
    
    Behind the scenes, it uses SerpAPI to access Google's results with an API key sourced from the environment variable 'SERPAPI_API_KEY'. It sends a query to the serpapi Google Search API and retrieves the search results. This tool is designed to use 'serpapi.com' as its base URL and pass the 'q' parameter for the search query. It sets the location parameter to 'United States' to ensure that the search results are localized to that region. The response returned by serpapi is a JSON object, from which the tool extracts the 'organic_results' key. The tool then converts the value associated with 'organic_results' into a JSON string and returns it as the output. This is useful for applications needing to process or display Google search results from the United States without the overhead of handling the entire API response.

    After using this tool, you must use another tool to scrape the links in the results. Be sure to retain the order of the Google Search results when scraping because Google is smart and has already sorted the results by relevance.
    """
    required_modules: ClassVar[List[str]] = ["google-search-results",]

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")
    
    query: str = Field(
        ..., description="The search query to send to the serpapi Google Search API."
    )

    def run(self):
        try:
            api_key = os.getenv('SERPAPI_API_KEY')
            if not api_key:
                raise ValueError("SERPAPI_API_KEY environment variable not set")
            params = {
                "q": self.query,
                "hl": "en",
                "gl": "us",
                "api_key": api_key
            }
            search = serpapi(params)
            results = search.get_dict()
            return json.dumps(results.get("organic_results"))
        except Exception as e:
            return json.dumps({"error": str(e)})