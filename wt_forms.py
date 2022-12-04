from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    title = StringField('Название: ', validators=[Length(min=1, max=25,
                                                         message='Название должно быть от 1 до 25 символов.')])
    ref = StringField('URL-slug: ', validators=[Length(min=1, max=25,
                                                       message='Слаг долен быть от 1 до 25 символов.')])
    submit = SubmitField('Добавить')


class PostForm(FlaskForm):
    title = StringField('Название: ', validators=[Length(min=1, max=25,
                                                         message='Название должно быть от 1 до 25 символов.')])
    ref = StringField('URL-slug: ', validators=[Length(min=1, max=25,
                                                       message='Слаг долен быть от 1 до 25 символов.')])
    text = TextAreaField('Post: ')
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    email = StringField('Login: ')
    psw = PasswordField('Password: ')
    submit = SubmitField('Войти')
