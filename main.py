from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from agent_tool_maker import AgentToolMaker
from werkzeug.serving import run_simple
import os
import traceback

os.system('pip install --upgrade pip')
app = Flask(__name__)
socketio = SocketIO(app)
agent_tool_maker = AgentToolMaker()

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
    execute_and_emit("howdy")
    # execute_and_emit("Which tools do you have access to? Keep it brief.")
    # execute_and_emit("create a very simple tool that uses pandas to sort data by any column.") 
    # don't do any file i/o...only use strings in/out.")
    # execute_and_emit("do a quick test of the pandas data sorter")
    # execute_and_emit("Let's get started with the encryption tool. Generate the key pair using the default key size, and then use the generated public key to encrypt a test message (\"Yo - wassup?\" and password \"password\"). After the keys are generated, perform the 'encrypt' operation with the sample message.")

@socketio.on('user_input')
def handle_user_input(data):
    execute_and_emit(data['input'])

if __name__ == "__main__":
    socketio.run(app, host='localhost', port=3000)
