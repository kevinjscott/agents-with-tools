from typing import ClassVar, List, Literal # IMPORTANT: ClassVar, List, and Literal are always required!
from instructor import OpenAISchema # IMPORTANT: OpenAISchema is always required! Note how the MyNewTool class is derived from OpenAISchema, not BaseModel
from pydantic import Field # IMPORTANT: Field is always required
from bs4 import BeautifulSoup # this import is just an example that has a non-trivial pip-installable module dependency

class MyNewTool(OpenAISchema): # IMPORTANT: the new class must be derived from OpenAISchema, not BaseModel. Don't you dare use BaseModel!
    """
    [Multi-paragraph description of the tool, its purpose, and how it works]
    
    Pros:
    - [list here]
    
    Cons:
    - [list here]
    
    [Instructions for when to use an alternative tool]
    """

    required_modules: ClassVar = [] # array of pip-installable package names that are needed to support the imports of this file
    # IMPORTANT: required_modules is always required and must always be a ClassVar. If there are no required modules, then use:
    # required_modules: ClassVar = []

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")
    # IMPORTANT: chain_of_thought param must be included in the new tool as an exact copy of the chain_of_thought param above. This is required for the AI to understand the context of the tool's usage. Do not change this line when creating the new tool...just copy it over.

    # below are some examples of how to define parameters for the new tool
    text: str = Field( 
        ..., description="The text to extract unique words from."
    )
    order: str = Field(
        default="asc", description="The order to return the words in, 'asc' for ascending or 'desc' for descending."
    )
    fast_or_slow: Literal["fast", "slow"] = Field(
        default="fast", description="Whether the function should run in fast mode or not." # use this approach rather than a bool
    )

    def run(self):  # IMPORTANT: this function must always be "def run(self):" and must always return a single string or int
        try:
            # code goes here
            # don't take any shortcuts: write ALL of the code with no "todo" items or "the rest of the code goes here" partial work
            return whatever # run() must always return a single string or integer
        except Exception as e:
            return "" # make this a useful error, but remember that run() must always return a single string or integer