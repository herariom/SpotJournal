from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == "__main__":
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()
