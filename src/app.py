from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/teste')
def handle_teste():
    return 'Hello, new route!'


if __name__ == '__main__':
    app.run(port=3001, host="0.0.0.0", debug=True)
