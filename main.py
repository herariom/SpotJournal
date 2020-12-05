from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/results')
def results():
    legend = "Results"
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]

    return render_template('results.html', values=values, labels=labels, legend=legend)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()
