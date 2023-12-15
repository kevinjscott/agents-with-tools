from instructor import OpenAISchema # [note for this template only] this is always required
from typing import ClassVar
from openai import OpenAI
from pydantic import Field

class AskAI(OpenAISchema):
    """
    This tool is designed to interact with the OpenAI API by sending a user's prompt and returning the AI's response. It is particularly useful when you need to generate text that is creative, contextually relevant, and coherent, including code. It can also be used to parse or extract information/data from the generated text. 
    
    The response can be up to 4000 tokens long. This makes it ideal for tasks that require long-form text generation, such as drafting articles, generating ideas, creating conversational agents, or writing code. It can also parse or extract information/data from text provided in the prompt, given the expected format and constraints are specified by the user.
    
    However, it's important to note that the tool is limited to text-based operations and does not support multi-modal tasks. It also does not provide options for different models or parameters, and cannot produce non-text responses such as images or audio. Therefore, it's best used when the task at hand is purely text-based and within the capabilities of the gpt-4-1106-preview model.

    IMPORTANT: This tool can not access the internet. It can only access the OpenAI API. If you need this tool to operate on data from the internet, you must first use a tool that extracts the data from the internet and then use that data as the input to this tool.
    
    Pros:
    - It's a simple and efficient way to interact with the OpenAI API.
    - It can parse or extract information/data from the generated text.
    - It can accept very long strings of data.
    
    Cons:
    - It doesn't provide options for different models or parameters.
    - It only operates on text i.e. it is not multi-modal.
    - It can not produce a response that is longer than 4000 tokens.
    - It can not produce non-text responses such as images or audio.
    - It can not access the internet.
    
    If you need a tool that provides more options, consider a different tool.
    
    Examples of sophisticated prompts:
    - "Translate the following English text to French: {{{{text}}}}."
    - "Write a poem about {{{{subject}}}}. Poem length: {length}"
    - "Summarize the following paragraph: {{{{paragraph}}}}. Response format: {format}"
    - "Extract the following information from the text: {{{{information}}}}. Expected format: {format}"
    - Note that these tend to be commands, not questions.
    
    The model used in this tool is gpt-4-1106-preview.
    """
    required_modules: ClassVar = [
        'openai'
    ]

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")

    prompt: str = Field(
        ..., description="The prompt to send to the OpenAI API."
    )

    def run(self):
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You write thoughtful, but very concise responses. You answer directly. If asked for code, just write the code and do not include any delimiters or separators (like ```) or markers identifying where the code section starts/ends. Seriously...only the code with absolutely no extra characters. No talk. Just do."},
                    {"role": "user", "content": self.prompt}
                ],
                temperature=0,
                max_tokens=4000,
            )
            completion = response.choices[0].message.content
            return completion
        except Exception as e:
            return f"Error: {str(e)}"
        except:
            return "An unexpected error occurred."