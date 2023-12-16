import concurrent.futures
import json
import time
from openai import OpenAI
from instructor import OpenAISchema
import glob
import importlib.util
import os
import re
import builtins
import textwrap
from flask_socketio import emit


client = OpenAI()

def show_json(obj):
    print(json.loads(obj.model_dump_json()))
    
def wprint(*args, width=170, **kwargs):
    """
    Custom print function that wraps text to a specified width.

    Args:
    *args: Variable length argument list.
    width (int): The maximum width of wrapped lines.
    **kwargs: Arbitrary keyword arguments.
    """
    wrapper = textwrap.TextWrapper(width=width)

    # Process all arguments to make sure they are strings and wrap them
    wrapped_args = [wrapper.fill(str(arg)) for arg in args]

    # Call the built-in print function with the wrapped text
    builtins.print(*wrapped_args, **kwargs)

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

        run_steps = client.beta.threads.runs.steps.list(
            thread_id=thread.id, run_id=run.id, order="asc"
        )

        for step in run_steps.data:
            step_details = step.step_details
            # print(json.dumps(show_json(step_details), indent=4))

        time.sleep(0.5)
    return run

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        if m.role == "user":
            print(f"\033[33m{m.role}: {m.content[0].text.value}\033[0m") # yellow
        elif m.role == "assistant":
            print(f"\033[34m{m.role}: {m.content[0].text.value}\033[0m") # blue
    print()

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def get_most_recent_response_text(thread):
    return client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value

def create_thread_and_run(assistant_id, user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

def get_completion(message, agent, funcs, thread):
    """
    Executes a thread based on a provided message and retrieves the completion result.

    This function submits a message to a specified thread, triggering the execution of an array of functions
    defined within a func parameter. Each function in the array must implement a `run()` method that returns the outputs.

    Parameters:
    - message (str): The input message to be processed.
    - agent (OpenAI Assistant): The agent instance that will process the message.
    - funcs (list): A list of function objects, defined with the instructor library.
    - thread (Thread): The OpenAI Assistants API thread responsible for managing the execution flow.

    Returns:
    - str: The completion output as a string, obtained from the agent following the execution of input message and functions.
    """

    print("🤖 get_completion sending message: " + message)
    emit('new_info', {'type': "agent", 'text': "🤖 " + message})

    # create new message in the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    # run this thread
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=agent.id,
    )

    while True:
      # wait until run completes
      while run.status in ['queued', 'in_progress']:
        # print("Getting run status")
        time.sleep(1)

        def retrieve_run():
            return client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Run the function with a watchdog timer of 5 seconds
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(retrieve_run)
            try:
                run = future.result(timeout=5)
            except concurrent.futures.TimeoutError:
                print("Run retrieval took longer than 5 seconds. Moving on.")
                return
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                return

      # function execution
      if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []
        for tool_call in tool_calls:
            print('\033[31m🛠️ ' + str(tool_call.function.name), '\033[0m') # red
            emit('new_info', {'type': "tool_call", 'text': '➡️🛠️ ' + str(tool_call.function.name) + "..."})
            func = next(iter([func for func in funcs if func.__name__ == tool_call.function.name]))

        try:
            func = func(assistant_id=agent.id, **eval(tool_call.function.arguments))
            print('\033[31m🛠️ tool_call: ' + func.chain_of_thought, '\033[0m') # red
            emit('new_info', {'type': "tool_call", 'text': '🧠 chain_of_thought: ' + func.chain_of_thought})
            for key in func.model_fields_set:
                if key != "chain_of_thought":
                    print(f'\033[31m🛠️ {key}: {getattr(func, key)}', '\033[0m') # red
                    emit('new_info', {'type': "tool_call", 'text': f'{key}:\n{getattr(func, key)}' if '\n' in getattr(func, key) else f'{key}: {getattr(func, key)}'})
            output = func.run()
        except Exception as e:
            output = "Error: " + str(e)

        print(f"\033[32m🛠️ {tool_call.function.name} output:\n", output, '\n', '\033[0m') # green
        emit('new_info', {'type': "tool_result", 'text': "⬅️🛠️ " + tool_call.function.name + "...\n" + output + "\n"})
        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

        # submit tool outputs
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
      # error
      elif run.status == "failed":
        raise Exception("Run Failed. Error: ", run.last_error)
      # return assistant message
      else:
        messages = client.beta.threads.messages.list(
          thread_id=thread.id
        )
        message = messages.data[0].content[0].text.value
        # emit('new_info', {'type': "agent", 'text': message})
        return message
      
def load_functions_and_tools(assistant_id):
    code_assistant_funcs = []
    files_in_functions = glob.glob("functions/[!\\.]*.py")
    files_in_subdirectories = glob.glob("functions/*/[!\\.]*.py")

    for file in files_in_functions + files_in_subdirectories:
        # Check for any missing imports and install them
        with open(file, 'r') as f:
            file_content = f.read()
            required_modules_start = file_content.find('required_modules: ClassVar = [')
            if required_modules_start != -1:
                required_modules_end = file_content.find(']', required_modules_start)
                required_modules_str = file_content[required_modules_start:required_modules_end+1]
                required_modules_str = required_modules_str.replace('\n', '')
                required_modules = eval(required_modules_str.split('=')[1].strip())
                for module in required_modules:
                    result = os.popen(f'pip show {module} | grep -e "Name" -e "Version"').read()
                    if not result:
                        os.system(f'pip install {module}')
                    else:
                        print(result.replace('\n', ' '))
        spec = importlib.util.spec_from_file_location("module.name", file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr_name in dir(module):
            attr_value = getattr(module, attr_name)
            if attr_name != "OpenAISchema" and isinstance(attr_value, type) and issubclass(attr_value, OpenAISchema):
                code_assistant_funcs.append(attr_value)

        tools_array = [{"type": "function", "function": func.openai_schema} for func in code_assistant_funcs]
    
    assistant = client.beta.assistants.update(
        assistant_id,
        tools=tools_array
    )
    tool_names = [tool['function']['name'] for tool in tools_array]
    print(tool_names)
    return code_assistant_funcs, tools_array, assistant
