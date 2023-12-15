from typing import ClassVar, List, Literal
from instructor import OpenAISchema
from pydantic import Field
import requests
from bs4 import BeautifulSoup
import json
import re

class WebScrapingTool(OpenAISchema):
    required_modules: ClassVar[List[str]] = ["requests", "bs4", "json", "re"]

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")
    
    url: str = Field(..., description="The URL of the web page to scrape.")
    tags: List[str] = Field(default=None, description="List of HTML tags to extract data from.")
    classes: List[str] = Field(default=None, description="List of HTML classes to extract data from.")
    ids: List[str] = Field(default=None, description="List of HTML element IDs to extract data from.")
    check_robots_txt: bool = Field(default=True, description="Whether to check the website's robots.txt file before scraping.")

    def run(self):
        if self.check_robots_txt and not self._is_scraping_allowed(self.url):
            return "Scraping is not allowed by the website's robots.txt policy."

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            data = {}
            if self.tags:
                for tag in self.tags:
                    data[tag] = [element.get_text(strip=True) for element in soup.find_all(tag)]
            if self.classes:
                for class_name in self.classes:
                    data[class_name] = [element.get_text(strip=True) for element in soup.find_all(class_=class_name)]
            if self.ids:
                for id_name in self.ids:
                    element = soup.find(id=id_name)
                    if element:
                        data[id_name] = element.get_text(strip=True)

            return json.dumps(data, ensure_ascii=False)
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def _is_scraping_allowed(self, url):
        parsed_url = requests.utils.urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        try:
            response = requests.get(robots_url)
            response.raise_for_status()
            return not bool(re.search(r"Disallow: /", response.text))
        except requests.RequestException:
            return False  # If we can't access robots.txt, proceed with caution.