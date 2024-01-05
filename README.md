# An Agent That Makes Its Own Tools

This project is a Python-based application that leverages OpenAI's GPT-4 model to create and utilize Python tools. It uses Flask and Flask-SocketIO for the web server and real-time communication, respectively. The application is designed to interact with the OpenAI API, execute shell commands, and create new Python tools based on user input.

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment (venv)

# Setting Up Your Environment

1. Clone the repository to your local machine.

2. Create a virtual environment in the project directory:
```python3 -m venv venv```

3. Activate the virtual environment:

- On macOS and Linux:
```source venv/bin/activate```

4. Install the required Python packages:
```pip install --upgrade pip```
```pip install -r requirements.txt```

# Environment Variables

This project requires the following environment variables:

- ASSISTANT1: The ID of your OpenAI assistant.
- OPENAI_API_KEY: Your OpenAI API key.
- SERPAPI_API_KEY: Your SerpAPI key for Google Search tool.

You can set these environment variables in your shell:
```export ASSISTANT1=your-assistant-id```
```export OPENAI_API_KEY=your-openai-api-key```
```export SERPAPI_API_KEY=your-serpapi-api-key```

Or, you can use a .env file in the project root directory and load it with python-dotenv.

# Running the Application

To run the application, execute the following command:
```python main.py```

The application will start a Flask server on localhost:3000. You can interact with the application by opening a web browser and navigating to http://localhost:3000. The application provides a user-friendly interface for creating and utilizing Python tools. Enjoy exploring the capabilities of this application!
