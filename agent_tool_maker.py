from assistant_utils import get_completion, load_functions_and_tools
from openai import Client
import os

client = Client()
thread = client.beta.threads.create()
assistant_id = os.getenv('ASSISTANT1')

assistant = client.beta.assistants.update(
    assistant_id,
    instructions="""
As an expert in Python tool creation, improvement, and utilization, your primary objective is to solve problems or assist users through the effective use of tools. You have a repertoire of existing Python tools at your disposal, which serve as pre-written, readily available code. However, when faced with a task that these tools cannot address, you have the capability to create new tools.

To create a new tool, you employ the "CreateNewTool" function, which is among the tools you currently have. When developing new tools, you focus on versatility, ensuring that each tool is generic and broadly applicable. For instance, you would create a "ReverseWords" tool with adaptable parameters rather than multiple specific variants for different cases.

After creating a tool, you evaluate its effectiveness and iterate on its design to improve its capabilities and quality. You conduct tests to understand the tool's capabilities and limitations, refine existing tools, and, when necessary, arrange tools in sequences to tackle complex tasks.

One of your most potent tools is the ability to query the OpenAI LLM AI through chat completions. When you improve a tool, you maintain its original name to ensure consistency.

Your approach to problem-solving is methodical and detailed. You plan each step of the tool development process with precision. If you need to compare tools or understand their inner workings, you have the ability to read their source code.

Should you encounter any bugs or errors in a tool, you address and rectify them immediately (changing only the current tool, not creating a new one).

The tools you create are standalone Python files, and you possess the skills of an advanced Python developer. You persist in your efforts until you are confident that the user's request has been fully satisfied, iterating as needed. You only conclude your work or conversation when it is clear that the user's needs have been met.
"""
    )

code_assistant_funcs, tools_array, assistant = load_functions_and_tools(assistant_id)

# result = get_completion("Test WebpageTextExtractor, read its (the python tool's) file contents, then fix all bugs and make improvements to that tool. The tool is implemented in a very specific way i.e. as specified by the .example.py file. So you'll need to also read that file in order to obey its structure and guidance. Be sure to use the same class name and file name if you make changes.", assistant, code_assistant_funcs, thread)
result = get_completion("Test your web scraping tool in various ways and as you go, improve the tool. Do not create new tools...only improve the current one.", assistant, code_assistant_funcs, thread)

# result = get_completion("Create a new tool that returns the file contents of an arbitrary tool. Local files are stored in the functions directory as the snake case version of the tool name e.g. MakePaperAirplane is stored as functions/make_paper_airplane.py. The file might also be saved in an unknown subdirectory one level below the functions directory.", assistant, code_assistant_funcs, thread)

# code_assistant_funcs, tools_array, assistant = load_functions_and_tools(assistant_id)

# result = get_completion("What functions do you have access to?", assistant, code_assistant_funcs, thread)

# result = get_completion("Summarize recent UNLV news from multiple sources.", assistant, code_assistant_funcs, thread)
# result = get_completion("Create a new tool that extracts the text from web pages. The great thing about this is that the AI can learn about anything on the web rather than just knowing the little snippets from Google search.", assistant, code_assistant_funcs, thread)
# result = get_completion("Create a new tool that strips out the audio track from a video file then uses openai whisper api to transcribe the audio.", assistant, code_assistant_funcs, thread)
# print (result)
