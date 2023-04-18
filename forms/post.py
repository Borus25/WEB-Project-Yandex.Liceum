from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    post_title = StringField('Название поста', validators=[DataRequired()])
    text_content = TextAreaField('Текст поста', validators=[DataRequired()])
    file = FileField("Файл")
    is_blog = BooleanField("Блог")
    is_training = BooleanField("Тренировка")
    is_recipe = BooleanField("Питание")
    submit = SubmitField('Добавить')