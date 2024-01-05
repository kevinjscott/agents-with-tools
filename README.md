# An Agent That Makes Its Own Tools

## Summary

This project uses an OpenAI Assistants API "tool" (was Function Calling) to create new tools and install/register them with the original agent that initiated the tool creation. That tool is tools/common/create_tool.py.

Each new tool is just a Python file that follows a specific format defined / described by tools/.example/example.py. The agent suggests the basic code and then the tool uses OpenAI to conform it to the necessary format.

## Setting Up Your Environment

1. Clone the repository to your local machine.

2. Create a virtual environment in the project directory:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

- On macOS and Linux:

```bash
source venv/bin/activate
```

4. Install the required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

This project requires the following environment variables:

- ASSISTANT1: The ID of your OpenAI assistant.
- OPENAI_API_KEY: Your OpenAI API key.
- SERPAPI_API_KEY: Your SerpAPI key for Google Search tool.

You can set these environment variables in your shell:

```bash
export ASSISTANT1=your-assistant-id
export OPENAI_API_KEY=your-openai-api-key
export SERPAPI_API_KEY=your-serpapi-api-key
```

Or, you can use a .env file in the project root directory and load it with python-dotenv.

## Running the Application

To run the application, execute the following command:

```bash
python main.py
```

Interact with the application at http://localhost:3000. Experiment with queries such as these:

```
What tools do you have access to?

create a very simple tool that uses pandas to sort data by any column. don't do any file i/o...only use strings in/out.

do a quick test of the pandas data sorter

Describe all the tools that you would need to create in order to create and manage your own Instagram account from scratch.
```

## Inspiration
- https://twitter.com/yoheinakajima/status/1730754111422034218
- https://github.com/VRSEN/agency-swarm
- https://github.com/jxnl/instructor

## Known issues and future exploration

GPT-4 tries to call functions with true/false when we need True/False. Seems like exactly what Pydantic should solve for us.

Needs to be better at writing code, testing it, iterating, etc.

Combine with other agents to create tools in parallel, plan out which tools are needed, keep things on the rails, ensure quality, etc.