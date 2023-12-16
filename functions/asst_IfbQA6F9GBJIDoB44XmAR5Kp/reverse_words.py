from typing import ClassVar
from instructor import OpenAISchema
from pydantic import Field

class ReverseWords(OpenAISchema):
    required_modules: ClassVar = []

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")
    text: str = Field(..., description="The text from which to reverse the order of words.")

    def run(self):
        try:
            words = self.text.split()
            words.reverse()
            reversed_text = ' '.join(words)
            return reversed_text
        except Exception as e:
            return f"An error occurred: {str(e)}"