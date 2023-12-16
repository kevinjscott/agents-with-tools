from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from agent_tool_maker import AgentToolMaker
from werkzeug.serving import run_simple

app = Flask(__name__)
socketio = SocketIO(app)
agent_tool_maker = AgentToolMaker()

code_run = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('new_info', {'type': "reset"})

    # emit("new_info",{"type":"agent","text":"\ud83e\udd16 Make a tool that reverses words in a string."})
    # emit("new_info",{"type":"tool_call","text":"\ud83d\udee0\ufe0f Calling CreateNewTool"})
    # emit("new_info",{"type":"tool_call","text":"🧠 chain_of_thought: To create a new tool for reversing words in a string, I will use Python's standard libraries. The str.split() method can be used to split the string into a list of words, and the list can then be reversed using the reversed() function or list slicing. After reversing the words, I will use the str.join() method to concatenate the reversed list of words back into a string. This tool should not require any external libraries."})
    # emit("new_info",{"type":"tool_call","text":"description: The ReverseWords tool takes a string input, reverses the order of the words within that string, and returns the result. It accomplishes this by splitting the string into a list of words, then reversing the list, and finally joining the list back into a string. This is useful for various text manipulation applications where the word order needs to be reversed."})
    # emit("new_info",{"type":"tool_call","text":"implementation_code:\ndef reverse_words(text):\n    # Split the text into a list of words\n    words = text.split()\n    # Reverse the list of words\n    reversed_words = reversed(words)\n    # Join the reversed list back into a string\n    reversed_text = ' '.join(reversed_words)\n    return reversed_text"})
    # emit("new_info",{"type":"tool_call","text":"file_name: reverse_words.py"})
    # emit("new_info",{"type":"tool_call","text":"implementation_code_modules: "})
    # emit("new_info",{"type":"tool_call","text":"class_name: ReverseWords"})
    # emit("new_info",{"type":"tool_call","text":"assistant_id: asst_IfbQA6F9GBJIDoB44XmAR5Kp"})
    # emit("new_info",{"type":"tool_result","text":"🤖 CreateNewTool output:\nfrom typing import ClassVar\nfrom instructor import OpenAISchema\nfrom pydantic import Field\n\nclass ReverseWords(OpenAISchema):\n    \"\"\"\n    The ReverseWords tool is designed to take a string input and reverse the order of the words within that string.\n    It does this by splitting the string into a list of words, reversing the list, and then joining the list back into a string.\n    This can be useful in various text manipulation tasks where reversing the word order is desired.\n\n    Pros:\n    - Simple and straightforward to use.\n    - Efficient for reversing the words in a string.\n\n    Cons:\n    - Limited to reversing words, does not handle punctuation or capitalization.\n    \n    Use an alternative tool if you need to maintain punctuation or capitalization in the original order.\n    \"\"\"\n\n    required_modules: ClassVar = [] \n\n    chain_of_thought: str = Field(\n        ..., description=\"Think step by step to determine the correct actions that are needed to be taken in order to complete the task.\"\n    )\n    \n    text: str = Field( \n        ..., description=\"The text whose words are to be reversed.\"\n    )\n\n    def run(self):\n        try:\n            words = self.text.split()\n            reversed_words = reversed(words)\n            reversed_text = ' '.join(reversed_words)\n            return reversed_text\n        except Exception as e:\n            return f\"An error occurred: {e}\"\n"})
    # emit("new_info",{"type":"agent","text":"The new Python tool for reversing words in a string has been successfully created. The `ReverseWords` tool accepts input as a string of text and outputs the text with the order of the words reversed. Here's a brief overview of how it works and its characteristics:\n\n```python\nclass ReverseWords(OpenAISchema):\n    \"\"\"\n    The ReverseWords tool is designed to take a string input and reverse the order of the words within that string.\n    It does this by splitting the string into a list of words, reversing the list, and then joining the list back into a string.\n    This can be useful in various text manipulation tasks where reversing the word order is desired.\n\n    Pros:\n    - Simple and straightforward to use.\n    - Efficient for reversing the words in a string.\n\n    Cons:\n    - Limited to reversing words, does not handle punctuation or capitalization.\n    \n    Use an alternative tool if you need to maintain punctuation or capitalization in the original order.\n    \"\"\"\n\n    def run(self, text: str):\n        words = text.split()\n        reversed_words = reversed(words)\n        reversed_text = ' '.join(reversed_words)\n        return reversed_text\n```\n\nThe tool is efficient for its intended purpose but keep in mind that it will not maintain punctuation or capitalization in the original order. If you need to reverse the words in a string while keeping other elements intact, you may need to use a different tool or modify this one accordingly."})


@socketio.on('start')
def handle_start():
    global code_run
    if not code_run:
        code_run = True
        result = agent_tool_maker.execute("Make a tool that reverses words in a string.")
        emit('new_info', {'type': "agent", 'text': "🤖 " + result})
        code_run = False

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=3000)
