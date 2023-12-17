from typing import ClassVar, List
from instructor import OpenAISchema
from pydantic import Field
import requests
from bs4 import BeautifulSoup

class ScrapeCurrentArticles(OpenAISchema):
    """
    This tool is designed to scrape the current articles from the main page of the PGA of America's official website.
    It uses the 'requests' module to make an HTTP GET request to the page URL, then parses the HTML content using 'BeautifulSoup'
    to extract the articles. The tool returns the titles, summaries, and URLs of the articles.
    
    Pros:
    - Easy to use and integrate into other systems.
    - Efficiently extracts relevant information without unnecessary data.
    
    Cons:
    - Limited to scraping the main page of the PGA of America's official website.
    - Dependent on the structure of the website, which may change over time.
    
    Use an alternative tool if you need to scrape data from websites with different structures or require more advanced scraping capabilities.
    """
    required_modules: ClassVar[List[str]] = ['requests', 'beautifulsoup4']

    chain_of_thought: str = Field(
        ..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task."
    )
    url: str = Field(
        ..., description="The URL of the PGA of America's official website to scrape articles from."
    )

    def run(self) -> List[dict]:
        try:
            return self.scrape_current_articles(self.url)
        except Exception as e:
            return f"An error occurred: {e}"

    def scrape_current_articles(self, url: str) -> List[dict]:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve content from URL: {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        current_articles = []
        for article in articles:
            title_element = article.find('h2')
            summary_element = article.find('p')
            link_element = article.find('a', href=True)

            title = title_element.text.strip() if title_element else "No title"
            summary = summary_element.text.strip() if summary_element else "No summary"
            article_url = link_element['href'].strip() if link_element else "No URL"

            current_articles.append({'title': title, 'summary': summary, 'url': article_url})

        return current_articles

# Note: The actual instantiation and usage of the ScrapeCurrentArticles class would be done outside of this class definition.