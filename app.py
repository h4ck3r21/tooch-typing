import random
import string
from collections import Counter
from time import sleep

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO
from Touch_typing_game import Player


class NoMatchingId(Exception):
    pass


class DuplicateId(Exception):
    pass


app = Flask(__name__)
socketio = SocketIO(app)
messages = ['herro']
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
users_online = []
users_offline = users_online[:]


def find_user_by_user_id(ID):
    print(f'checking if {ID} in {users_online}')
    for user in users_online:
        print(f'is {user.id} equal to {ID}; {user.id == ID}')
        if user.id == ID:
            print(f'found user')
            return user
    users_online.append(Player('Unknown', ID))
    return find_user_by_user_id(ID)


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


@socketio.on('keypress')
def keypress(json):
    print(f'online users: {users_online}')
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
    global users_offline
    users_offline = users_online[:]
    print('user disconnection')
    socketio.emit('user disconnect')


@socketio.on('connecting')
def connect(json):
    sleep(5)
    remove_duplicates()
    if json['userID'] in [user.id for user in users_online]:
        users_online.remove(find_user_by_user_id(json['userID']))
    socketio.emit('log', 'user connected')
    print('received connection: ' + str(json))
    player = Player(json['username'], json['userID'])
    socketio.emit('new user', json['userID'])
    enemy_ids = {'id': json['userID']}
    i = 0
    for user in users_online:
        print(f'id:{user.id}')
        enemy_ids[i] = user.id
        i += 1
    enemy_ids['len'] = i
    socketio.emit('connection', enemy_ids)
    print('added user')
    users_online.append(player)


def remove_duplicates():
    if [item for item, count in Counter([user.id for user in users_online]).items() if count > 1]:
        for ID in [item for item, count in Counter([user.id for user in users_online]).items() if count > 1]:
            users_online.remove(find_user_by_user_id(ID))
            remove_duplicates()


@socketio.on('online')
def check_online(ID):
    remove_duplicates()
    if ID in [user.id for user in users_online]:
        users_online.remove(find_user_by_user_id(ID))
    print(f'{ID} is online')
    if find_user_by_user_id(ID) in users_offline:
        users_offline.remove(find_user_by_user_id(ID))
    if len(users_offline) == 1:
        print(f'{users_offline[0].name} disconnected')
        users_online.remove(users_offline[0])
        socketio.emit('log', 'user_disconected')
    enemy_ids = {'id': ID}
    i = 0
    for user in users_online:
        print(f'id:{user.id}')
        enemy_ids[i] = user.id
        i += 1
    enemy_ids['len'] = i
    print('checking if online')
    socketio.emit('connection', enemy_ids)
    socketio.emit('new user', ID)


@app.route("/send-message", methods=["POST"])
def receive():
    global messages
    messages.append(request.form["mytext"])
    return redirect(url_for("hello"))


if __name__ == '__main__':
    socketio.run(app)
