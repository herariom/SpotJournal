from flask import Flask, render_template, url_for, request, make_response
import os
from random import randrange
from werkzeug.utils import redirect

from chart import generate_chart
from forms import ContactForm, FinishedForm, DateForm
import pymysql.cursors

from song_data import SongData
from sql import SpotSQL

import sp


app = Flask(__name__)

sess_key = os.urandom(32)

# Generate session key
app.secret_key = sess_key

app.config['SECRET_KEY'] = sess_key
app.config['WTF_CSRF_ENABLED'] = False

labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Angry"]

db = SpotSQL()


@app.route('/journal', methods=('GET', 'POST'))
def journal():
    form = DateForm()

    if request.method == 'POST' and form.validate_on_submit():

        spot = SpotSQL()
        data = spot.get_user_songs(sp.get_user_id())

        return render_template('journal.html', data=generate_chart(request.cookies.get('prevEmotion')), labels=labels)


    return render_template('journal.html')


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('listen.html')


@app.route('/finished', methods=('GET', 'POST'))
def finished():
    form = FinishedForm()

    if request.method == 'POST' and form.validate_on_submit():
        return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion')), labels=labels)

    return render_template('finished.html', form=form)


@app.route('/form', methods=('GET', 'POST'))
def questionnaire():
    form = ContactForm()

    if request.method == 'POST' and form.validate_on_submit():
        [oauth, spot_obj] = sp.get_spotipy_objs()
        url = sp.get_random_song(db.get_user_songs(spot_obj.current_user()['id']))
        resp = make_response(render_template('listen.html', state='completed', url=url))
        resp.set_cookie('prevEmotion', form.current_emotion.data)
        return resp

        #if state == 'finished':

            #return render_template('results.html', data=generate_chart(request.cookies.get('prevEmotion'), form.current_emotion.data), labels=labels)
        #else:
    return render_template('form.html', form=form)

@app.route('/spotify', methods=('GET', 'POST'))
def spotify():
    sp.spotify()
    return redirect(url_for('questionnaire'))

@app.route('/', methods=('GET', 'POST'))
def index():

    return render_template('index.html')


if __name__ == "__main__":
    app.run()
