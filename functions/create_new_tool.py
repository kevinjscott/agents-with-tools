from typing import ClassVar, List, Literal
from instructor import OpenAISchema
from pydantic import Field
import os
from openai import OpenAI
from assistant_utils import load_functions_and_tools


class CreateNewTool(OpenAISchema):
    """
    This tool is designed to automate the creation of new Python tools using an existing tool template. Tools are Python files that can be used by the LLM in the future.
    
    This tool reads the contents of a predefined example Python file template '.example.py' to use as a style guide. It then generates a new tool (a Python file) that implements the desired functionality while adhering to the style of the example file. Then it saves the new tool to disk for future use.

    IMPORTANT: Do not specify an assistant_id parameter.

    IMPORTANT: If you're not 100% certain about which libraries / modules to use or exactly how to use them, be sure to do web extensive research first and then use that to inform your description of the desired functionality. You should also do web research to find the best libraries / modules to use for the desired functionality.
    
    Pros:
    - Automates the process of creating new tools i.e. code generation, ensuring consistency in coding style.
    - Saves time by eliminating the need to manually write boilerplate code.
    - Gives you (the LLM) new tools that you can use in the future to solve problems and expand your capabilities.
    
    Cons:
    - The success of the tool is heavily dependent on the quality and relevance of the example file.
    - Requires a clear and precise description of the desired functionality.
    
    For best results, ensure the example file accurately reflects the intended code style and the functionality description is detailed.
    """
    required_modules: ClassVar = []

    chain_of_thought: str = Field(..., description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.")

    assistant_id: str = Field(default=None, validate_default=True)
    class_name: str = Field(..., description="The TitleCase name of the new tool's class. This must always use exactly the same words as file_name, but be written in TitleCase.")
    file_name: str = Field(..., description="The snake_case name of the python file to save, with extension. This must always use exactly the same words as class_name, but be written in snake_case.")
    description: str = Field(..., description="A highly detailed description of the new tool's functionality. Before writing this, you should consider which architecture and design patterns to use as well as research the best libraries to use.")
    implementation_code: str = Field(..., description="The fully functional python code that will be sent to openai along with the .example.py file.")
    implementation_code_modules: str = Field(..., description="The names of the pip-installable modules needed to run your implementation_code. All modules will be incorporated into the new tool's Python code.")

    def run(self):
        try:
            prompt = ""
            prompt += "<<<<<-" + self.description + "->>>>>\n"
            prompt += "<<<<<--" + self.implementation_code + "-->>>>>\n"
            prompt += "<<<<<---" + str(self.required_modules) + "--->>>>>\n"

            with open('functions/.example.py', 'r') as file:
                example_code = file.read()
            prompt += "<<<<<=" + example_code + "=>>>>>\n"

            client = OpenAI()
            system_prompt = """Write unformatted python code for class """ + self.class_name + """(OpenAISchema) with params, required_modules, and run() method.

You only write fully functional python code tools without todo's or lazy shortcuts. The python code will be a tool that implements <<<<<-functionality->>>>>. The tool must be written in the exact same style / format as <<<<<=template=>>>>>. A suggested implementaion is provided <<<<<--implementation_code->>>>>, but since you only write perfect code, you should check it for issues and make it more robust, performant, and high quality. The pip-installable required modules to run this code/tool are <<<<<---provided--->>>>> and you will need to incorporate those into the Python file you write (per the template). If you make any code changes, be sure to make the corresponding changes to the modules. IMPORTANT: your response is not allowed to have any markdown in it...only the actual python code.

You may not start with '''python."""

            response = client.chat.completions.create(
              model="gpt-4-1106-preview",
              max_tokens=4000,
              temperature=0.0,
              messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": system_prompt + "\n\n" + prompt},
              ]
            )

            new_tool_content = response.choices[0].message.content
            # print(new_tool_content)

            # Clean out the delimiters / markdown / extra chars from the new_tool_content
            start_index = new_tool_content.find('```python')
            end_index = new_tool_content.rfind('```')
            if start_index != -1 and end_index != -1:
                new_tool_content = new_tool_content[start_index + len('```python'):end_index].strip()

            directory = f'functions/{self.assistant_id}'
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(f'{directory}/{self.file_name}', 'w') as file:
                file.write(new_tool_content)

            load_functions_and_tools(self.assistant_id)

            return new_tool_content

        except Exception as e:
            return str(e) # Return the exception as a string
