from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from agent_tool_maker import AgentToolMaker
from werkzeug.serving import run_simple
import os

os.system('pip install --upgrade pip')
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

def execute_and_emit(input):
    emit('new_info', {'type': "status_running"})
    result = agent_tool_maker.execute(input)
    emit('new_info', {'type': "agent", 'text': "🤖 " + str(result)})
    print("🤖 " + str(result))
    emit('new_info', {'type': "status_stopped"})

@socketio.on('start')
def handle_start():
    execute_and_emit("Which tools do you have access to?")

@socketio.on('user_input')
def handle_user_input(data):
    execute_and_emit(data['input'])

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=3000)
