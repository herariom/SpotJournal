from flask import Flask, render_template, url_for, request
import os

from werkzeug.utils import redirect

from forms import ContactForm
import pymysql.cursors

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

connection = pymysql.connect(host='10.43.112.2',
                             user='root',
                             password='test',
                             db='test',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        # sql = "CREATE TABLE `users` (`email` VARCHAR(20), `password` VARCHAR(20))"
        # cursor.execute(sql)
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()