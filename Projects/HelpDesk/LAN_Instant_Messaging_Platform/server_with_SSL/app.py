from flask import Flask, render_template
from flask_socketio import SocketIO, send
from OpenSSL import SSL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_certificate('path/to/cert.pem')
context.use_privatekey('path/to/key.pem')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, ssl_context=context)
