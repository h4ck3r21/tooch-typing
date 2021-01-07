import random
import string
from time import sleep

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO
from touch_typing_game import Player


class NoMatchingId(Exception):
    pass


app = Flask(__name__)
socketio = SocketIO(app)
messages = ['herro']
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
users_online = []


def find_user_by_user_id(ID):
    print(f'checking if {ID} in {users_online}')
    for user in users_online:
        print(f'is {user.id} equal to {ID}; {user.id == ID}')
        if user.id == ID:
            print(f'found user')
            return user
    raise NoMatchingId('no user found with id')


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


@socketio.on('keypress')
def keypress(json):
    print('received keypress: ' + str(json))
    find_user_by_user_id(json['userID']).get_message(json['input'])
    player = find_user_by_user_id(json['userID'])
    player.check()
    if player.cor_msg != '':
        errors = player.message.split(player.cor_msg, 1)
    else:
        errors = player.message
    socketio.emit('paragraph', {"para": player.remaining_char,
                                "cor": player.cor_msg,
                                "errors": errors,
                                "id": json['userID'],
                                })
    if player.is_correct:
        print(f'{json["userID"]} fixes all errors')
        socketio.emit('fix', json['userID'])
    else:
        print(f'{json["userID"]} made an error')
        socketio.emit('error', json['userID'])


@app.route("/setcookie", methods=['POST'])
def set_cookie():
    user = request.form['name']
    print(f'setting cookie for user {user}')
    resp = make_response(render_template('set-cookie.html'))
    resp.set_cookie('userName', user)
    resp.set_cookie('userID', get_random_string(16))
    return resp


@app.route("/paragraph/<userid>")
def paragraph(userid):
    try:
        return render_template('paragraph.html',
                               paragraph=find_user_by_user_id(userid).para,
                               userid=userid,
                               )
    except NoMatchingId:
        sleep(1)
        return paragraph(userid)


@app.route("/")
def hello():
    name = request.cookies.get('userName')
    userID = request.cookies.get('userID')
    if not name:
        return render_template('cookies.html')
    print('rendering home page')
    return render_template('homepage.html', name=name, userid=userID)


@socketio.on('disconnect')
def disconnected():
    global users_online
    print('user disconnection')
    socketio.emit('user disconnect')


@socketio.on('connecting')
def connect(json):
    user_name = json['username']
    socketio.emit('log', f'{user_name} connected')
    print('received connection: ' + str(json))
    player = Player(user_name, json['userID'])
    socketio.emit('new user', json['userID'])
    enemy_ids = {'id': json['userID']}
    i = 0
    for user in users_online:
        print(f'id:{user.id}')
        enemy_ids[i] = user.id
        i += 1
    enemy_ids['len'] = i
    socketio.emit('connection', enemy_ids)
    users_online.append(player)


@socketio.on('online')
def check_online(ID):
    print(f'{ID} is online')
    users_offline = users_online[:]
    users_offline.remove(find_user_by_user_id(ID))
    if len(users_offline) == 1:
        print(f'{users_offline[0].name} disconnected')
        users_online.remove(users_offline[0])
        socketio.emit('log', 'user_disconected')
    socketio.emit('new user', ID)
    enemy_ids = {'id': ID}
    i = 0
    for user in users_online:
        print(f'id:{user.id}')
        enemy_ids[i] = user.id
        i += 1
    enemy_ids['len'] = i
    socketio.emit('connection', enemy_ids)
    socketio.emit('new user', ID)


@app.route("/send-message", methods=["POST"])
def receive():
    global messages
    messages.append(request.form["mytext"])
    return redirect(url_for("hello"))


if __name__ == '__main__':
    socketio.run(app)
