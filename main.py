from flask import Flask, render_template, url_for, request
import os

from werkzeug.utils import redirect

from forms import ContactForm

app = Flask(__name__)


@app.route('/results')
def result():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]

    return render_template('results.html', values=values, labels=labels, legend=legend)


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
    # Generate session key
    app.secret_key = os.urandom(24)

    app.run()
