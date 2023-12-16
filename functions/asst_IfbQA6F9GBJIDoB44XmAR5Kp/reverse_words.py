from typing import ClassVar
from instructor import OpenAISchema
from pydantic import Field

class ReverseWords(OpenAISchema):
    required_modules: ClassVar = []

    chain_of_thought: str = Field(
        ..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task."
    )
    text: str = Field(
        ..., description="The text whose words are to be reversed in order."
    )

    def run(self):
        try:
            words_list = self.text.split()
            words_list.reverse()
            reversed_text = ' '.join(words_list)
            return reversed_text
        except Exception as e:
            return f"An error occurred: {str(e)}"