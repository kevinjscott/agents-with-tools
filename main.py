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
    # emit('new_info', {"type":"tool_call","text":"description: A tool that takes a string of text as input, splits the text into individual words, reverses the order of the words, and then joins them back into a single string. The output is a string with all the original words in reverse order."})

@socketio.on('start')
def handle_start():
    global code_run
    if not code_run:
        code_run = True
        emit('new_info', {'type': "status_running"})
        result = agent_tool_maker.execute("Make a tool that reverses words in a string.")
        emit('new_info', {'type': "agent", 'text': "🤖 " + result})
        code_run = False
        emit('new_info', {'type': "status_stopped"})

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=3000)
