from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()
