"""
Админ панель.

Реализован функционал добавления и удаление категории, статьи.
"""
import sqlite3
from os import getenv
from functools import wraps

from flask import Blueprint, request, redirect, render_template, url_for, flash, session
import markdown

from utils.wt_forms import LoginForm, CategoryForm, PostForm
from utils.sqlacchemy_models import db, Posts, Categories

LOGIN = 'admin'
PASSWORD = getenv('ADMIN_PASS')


admin = Blueprint('admin', __name__, template_folder='templates')


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('admin_logged'):
            return func(*args, **kwargs)
        return redirect(url_for('.login'))
    return wrapper


@admin.route('/')
@login_required
def index():
    form = LoginForm()
    categories = Categories.query.all()
    posts = Posts.query.all()
    return render_template('admin/index.html', posts=posts, categories=categories, form=form)


@admin.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        psw = form.psw.data
        if name == LOGIN and psw == PASSWORD:
            login_admin()
            return redirect(url_for('.index'))  # так указываем index из текущего модуля, без точки будет из приложения
        else:
            flash('Неправильный логин или пароль', 'error')
    return render_template('admin/login.html', form=form, categories=Categories.query.all())


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if session.get('admin_logged'):
        logout_admin()
    return redirect(url_for('.login'))


@admin.route('/add-category', methods=['POST', 'GET'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Categories(title=form.title.data, ref=form.ref.data)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('category'))
        except sqlite3.Error:
            db.session.rollback()  # откатываем все изменения
            flash('Ошибка записи в базу данных', 'error')
    return render_template('add_category.html', form=form, categories=Categories.query.all())


@admin.route('/add-post', methods=['POST', 'GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        cat = Categories.query.get(int(request.form['cat']))
        post = Posts(title=form.title.data,
                     ref=form.ref.data,
                     text=markdown.markdown(form.text.data),
                     category_id=int(request.form['cat']))
        try:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post', category=cat.ref, post=post.ref))
        except sqlite3.Error:
            db.session.rollback()  # откатываем все изменения
            flash('Ошибка записи в базу данных', 'error')
    return render_template('add_post.html', form=form, categories=Categories.query.all())


@admin.route('del-post/<path:post>')
@login_required
def del_post(post):
    post_to_del = Posts.query.filter_by(ref=post).first()
    db.session.delete(post_to_del)
    db.session.commit()
    return redirect(url_for('.index'))


@admin.route('del-category/<path:category>')
@login_required
def del_category(category):
    cat_to_del = Categories.query.filter_by(ref=category).first()
    if Posts.query.filter_by(category_id=cat_to_del.id).first() is None:
        db.session.delete(cat_to_del)
        db.session.commit()
    else:
        flash('Очистите категорию перед удалением!', 'Сообщение')
    return redirect(url_for('.index'))
