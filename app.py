from flask import Flask

app = Flask(__name__)
conversation = ['']
new_message = ''
message_num = 0


@app.route('/get-message')
def chat():
    global new_message
    message = new_message
    return message + f'mnum:{message_num}'


@app.route('/send-message/<name>/<message>')
def receive_message(name, message):
    global message_num
    global new_message
    conversation.append(f'[{name}] {message}')
    message_num += 1
    new_message = f'[{name}] {message}'
    return '<html><body><h1>message sent</h1></body></html>'


@app.route('/get-previous-messages')
def send_previous_messages():
    return '\n'.join(conversation) + f'mnum:{message_num}'


@app.route('/')
def entire_conversation():
    return str(conversation)


if __name__ == '__main__':
    app.run()
