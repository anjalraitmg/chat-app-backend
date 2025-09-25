from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)
# Add CORS to allow our React app to connect
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Create the Socket.IO server, wrapping the Flask app
socketio = SocketIO(app, cors_allowed_origins="*")

# A dictionary to store connected users {session_id: username}
connected_users = {}

@socketio.on('connect')
def handle_connect():
    """This function is called when a user opens the webpage."""
    print(f'Client connected! SID: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """This function is called when a user closes the webpage."""
    print(f'Client disconnected! SID: {request.sid}')
    # Remove the user from our dictionary if they exist
    if request.sid in connected_users:
        username = connected_users.pop(request.sid)
        print(f'User {username} has left.')
        # Broadcast the new user list to all remaining clients
        emit('user_list', list(connected_users.values()), broadcast=True)

@socketio.on('join')
def handle_join(username):
    """This function is called when a user logs in with their name."""
    # Store the user's name with their unique session ID
    connected_users[request.sid] = username
    print(f'User {username} has joined. SID: {request.sid}')
    print(f'Current users: {list(connected_users.values())}')
    # Broadcast the new, updated list of users to ALL clients
    emit('user_list', list(connected_users.values()), broadcast=True)

@socketio.on('message')
def handle_message(data):
    """This function is called when a server receives an event named 'message'."""
    # data will be an object like {'author': 'user', 'message': 'text'}
    print(f'Received message from {data["author"]}: {data["message"]}')
    
    # The emit function will broadcast the entire data object to ALL connected clients.
    emit('message', data, broadcast=True)

# This is the entry point to run our server
if __name__ == '__main__':
    print("Starting server...")
    # For production, we'll use a different command, but this is fine for local dev
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)