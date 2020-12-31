from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)
messages = ['herro']


@app.route("/")
def hello():
    print('rendering home page')
    return render_template('homepage.html')


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ' + str(json))
    socketio.emit('my response', json)


@app.route("/send-message", methods=["POST"])
def receive():
    global messages
    messages.append(request.form["mytext"])
    return redirect(url_for("hello"))


if __name__ == '__main__':
    socketio.run(app)
