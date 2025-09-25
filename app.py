from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Create Socket.IO server
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Socket Events ---
@socketio.on('connect', namespace='/chat')
def handle_connect():
    client_id = request.sid
    print(f'🔌 Client connected: {client_id}')

@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
    client_id = request.sid
    print(f'❌ Client disconnected: {client_id}')

@socketio.on('message', namespace='/chat')
def handle_message(data):
    """Handle chat messages safely"""
    try:
        author = data.get("author", "Anonymous")
        msg = data.get("message", "").strip()
        if msg:
            print(f'💬 {author}: {msg}')
            emit('message', {"author": author, "message": msg}, broadcast=True, namespace='/chat')
    except Exception as e:
        print(f"⚠️ Error handling message: {e}")

# Run the server
if __name__ == '__main__':
    print("🚀 Chat server running on http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
