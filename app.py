from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
message = 'herro'


@app.route("/")
def hello():
    return render_template('homepage.html', message=message)


@app.route("/send-message", methods=["POST"])
def receive():
    global message
    message += '<br>\n' + request.form["mytext"]
    return redirect(url_for("hello"))


if __name__ == '__main__':
    app.run()
