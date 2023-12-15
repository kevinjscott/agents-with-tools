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
    # if not code_run:
        # emit('new_info', {'type': "agent", 'text': "howdy"})
        # emit('new_info', {'type': "tool_call", 'text': "tool call"})
        # emit('new_info', {'type': "tool_result", 'text': "tool result tool result tool result tool result tool resulttool result tool result tool resulttool resulttool result"})

@socketio.on('start')
def handle_start():
    global code_run
    if not code_run:
        code_run = True
        result = agent_tool_maker.execute("What time is it?")
        emit('new_info', {'type': "agent", 'text': result})
        code_run = False

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=3000)
