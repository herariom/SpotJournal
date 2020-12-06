from flask import Flask, render_template, url_for, request
import os
from random import randrange
from werkzeug.utils import redirect

from forms import ContactForm
import pymysql.cursors

from song_data import SongData

app = Flask(__name__)


@app.route('/results')
def result():
    labels = ["Angry", "Happy", "Sad", "Scared", "Confused"]

    testdata = []

    user_values = [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)]
    print(user_values)
    testdata.append(SongData('Your Emotions', user_values, 220, 0, 0))

    for x in range(1, 10):
        testdata.append(SongData(('User ' + str(x)), [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)], randrange(30, 255, 5), randrange(30, 255, 5), randrange(30, 255, 5)))

    return render_template('results.html', data=testdata, labels=labels)


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('results.html')


@app.route('/', methods=('GET', 'POST'))
def index():

    form = ContactForm()

    if request.method == 'POST' and form.validate():
        return redirect(url_for('success'))

    return render_template('index.html', form=form)


if __name__ == "__main__":

    sess_key = os.urandom(24)

    # Generate session key
    app.secret_key = sess_key

    app.config['SECRET_KEY'] = sess_key

    app.run()