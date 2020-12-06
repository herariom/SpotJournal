from flask import Flask, render_template, url_for, request, make_response
import os
from random import randrange
from werkzeug.utils import redirect

from chart import generate_chart
from forms import ContactForm
import pymysql.cursors

from song_data import SongData

app = Flask(__name__)

sess_key = os.urandom(32)

# Generate session key
app.secret_key = sess_key

app.config['SECRET_KEY'] = sess_key

labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Angry"]


# def generate_chart():
#     labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Unsure"]
#
#     testdata = []
#
#     user_values = [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)]
#     print(user_values)
#     testdata.append(SongData('Your Emotions', user_values, 220, 0, 0))
#
#     for x in range(1, 10):
#         testdata.append(SongData(('User ' + str(x)), [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)], randrange(30, 255, 5), randrange(30, 255, 5), randrange(30, 255, 5)))
#
#     return render_template('results.html', data=testdata, labels=labels)


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('listen.html')


@app.route('/form/<state>', methods=('GET', 'POST'))
def questionnaire(state):
    form = ContactForm()

    if request.method == 'POST' and form.validate_on_submit():
        if state == 'finished':

            return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion'), form.current_emotion.data), labels=labels)
        else:
            resp = make_response(render_template('listen.html'))
            resp.set_cookie('prevEmotion', form.current_emotion.data)
            return resp

    return render_template('form.html', state=state, form=form)


@app.route('/', methods=('GET', 'POST'))
def index():

    return render_template('index.html')


if __name__ == "__main__":
    app.run()
