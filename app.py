from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
messages = ['herro']


@app.route("/")
def hello():
    return render_template('homepage.html', messages=messages)


@app.route("/send-message", methods=["POST"])
def receive():
    global messages
    messages.append(request.form["mytext"])
    return redirect(url_for("hello"))


if __name__ == '__main__':
    app.run()
