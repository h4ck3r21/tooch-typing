from flask import Flask

app = Flask(__name__)
conversation = ['']
new_message = ''
message_num = 0


@app.route('/')
def home():
    return "<html><body\><h1>hello<h1\><body\><html>"


if __name__ == '__main__':
    app.run()
