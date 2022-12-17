"""
Формы для создания постов, категорий и авторизации.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length


class CategoryForm(FlaskForm):
    title = StringField('Название: ', validators=[Length(min=1, max=25,
                                                         message='Название должно быть от 1 до 25 символов.')])
    ref = StringField('URL-slug: ', validators=[Length(min=1, max=25,
                                                       message='Slug долен быть от 1 до 25 символов.')])
    submit = SubmitField('Добавить')


class PostForm(FlaskForm):
    title = StringField('Название: ', validators=[Length(min=1, max=80,
                                                         message='Название должно быть от 1 до 80 символов.')])
    ref = StringField('URL-slug: ', validators=[Length(min=1, max=80,
                                                       message='Slug долен быть от 1 до 80 символов.')])
    text = TextAreaField('Post: ')
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    name = StringField('Login: ')
    psw = PasswordField('Password: ')
    submit = SubmitField('Войти')
