from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)
messages = ['herro']


@app.route('/setcookie', methods=['POST'])
def set_cookie():
    user = request.form['name']
    print(f'setting cookie for user {user}')
    resp = make_response(render_template('set-cookie.html'))
    resp.set_cookie('userID', user)
    return resp


@app.route("/")
def hello():
    name = request.cookies.get('userID')
    if not name:
        return render_template('cookies.html')
    print('rendering home page')
    return render_template('homepage.html', name=name)


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
