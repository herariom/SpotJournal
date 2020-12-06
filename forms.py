from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email

from wtforms.fields.html5 import DateField

class ContactForm(FlaskForm):
    """Contact form."""
    current_day = StringField(
        'How has your day been so far?',
        [
            DataRequired(),
            Length(min=4,
                   message='Your message is too short.')
        ]
    )
    current_emotion = SelectField(
        'What emotion are you feeling at the moment',
        [DataRequired()],
        choices=[
            ('Happy', 'Happy'),
            ('Excited', 'Excited'),
            ('Calm', 'Calm'),
            ('Sad', 'Sad'),
            ('Stressed', 'Stressed'),
            ('Angry', 'Angry')
        ]
    )
    emotion_explanation = StringField(
        'Why are you feeling this way?',
        [
            DataRequired(),
            Length(min=4,
                   message='Your message is too short.')
        ]
    )
    submit = SubmitField('Submit')


class FinishedForm(FlaskForm):
    """Second questionnaire."""
    emotion_response = SelectField(
        'Did the song make you feel better, neutral, or worse?',
        [DataRequired()],
        choices=[
            ('Better', 'Better'),
            ('Neutral', 'Neutral'),
            ('Worse', 'Worse')
        ]
    )
    emotion_conveyed = StringField(
        'What emotion does this song convey to you?',
        [
            DataRequired(),
            Length(min=4,
                   message='Your message is too short.')
        ]
    )
    submit = SubmitField('Submit')


## Date picker
class DateForm(FlaskForm):
    dt = DateField('DatePicker', format='%Y-%m-%d')
    submit = SubmitField('Submit')
