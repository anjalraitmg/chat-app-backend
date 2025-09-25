# backend/app.py - MODIFIED FOR PRODUCTION
import os
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)

# Get the frontend URL from an environment variable for security
# Use a default for local development
frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

# Make CORS more secure: only allow the frontend to connect
CORS(app, resources={r"/*": {"origins": frontend_url}})
socketio = SocketIO(app, cors_allowed_origins=frontend_url)

@socketio.on('connect')
def handle_connect():
    print('Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socketio.on('message')
def handle_message(data):
    print(f'Received message from {data["author"]}: {data["message"]}')
    emit('message', data, broadcast=True)

# We no longer need the __main__ block for production
# Gunicorn will run the 'app' object directly