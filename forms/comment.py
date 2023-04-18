from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Прокомментировать')