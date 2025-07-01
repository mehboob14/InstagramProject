from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, it works!"


@app.route("test_route")
def test():
    return "sample test output"