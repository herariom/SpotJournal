from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email


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
            ('Happy', 'happy'),
            ('Sad', 'sad'),
            ('Unsure', 'unsure')
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