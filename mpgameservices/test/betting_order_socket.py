import socketio
from flask import Flask

sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.event
def connect (sid, environ, auth):
    print (f"Someone connected: {sid}")
    sio.emit('initial_data', {'bettingOrder': [1, 2, 3, 4, 5, 6]}, sid)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8002)