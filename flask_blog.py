"""
Блог о web разработке на Flask.
"""
import sqlite3
from os import getenv
from datetime import datetime

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from wt_forms import CategoryForm, PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False       # если есть ошибка в консоли

# app.register_blueprint(category, url_prefix='/')

db = SQLAlchemy(app)    # подключаем базу данных к нашему приложению


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    ref = db.Column(db.String(25), unique=True)

    def __repr__(self):
        return self.title


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=True)
    ref = db.Column(db.String(25), nullable=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship('Categories',
                               backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return self.title


# @app.route('/')
# def index():
#     categories = Categories.query.all()
#     return render_template('base.html', categories=categories)


@app.route('/add-category', methods=['POST', 'GET'])
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


@app.route('/add-post', methods=['POST', 'GET'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        cat = Categories.query.get(int(request.form['cat']))
        post = Posts(title=form.title.data,
                     ref=form.ref.data,
                     text=form.text.data,
                     category_id=int(request.form['cat']))
        try:
            db.session.add(post)
            db.session.commit()
            print(f'{cat.ref=} \t {post.ref=}')
            return redirect(url_for('post', category=cat.ref, post=post.ref))
        except sqlite3.Error:
            db.session.rollback()  # откатываем все изменения
            flash('Ошибка записи в базу данных', 'error')
    return render_template('add_post.html', form=form, categories=Categories.query.all())


@app.route('/')
@app.route('/<path:category>')
def category(category=None):
    cat = Categories.query.filter_by(ref=category).first()
    if cat is None:
        cat = Categories.query.get(1)
    posts = Posts.query.filter_by(category_id=cat.id).all()
    return render_template('category.html', posts=posts, cat=cat, categories=Categories.query.all())


@app.route('/<path:category>/<path:post>')
def post(category, post):
    cat = Categories.query.filter_by(ref=category).first()
    # posts = Posts.query.filter_by(category_id=cat.id, ref=post).first()
    posts = Posts.query.filter_by(category_id=cat.id).all()
    return render_template('post.html', posts=posts, current_post=post, cat=cat, categories=Categories.query.all())


if __name__ == '__main__':
    app.run(debug=True)

    # создаем базу данных и таблицы в ней
    # with app.app_context():
    #     db.create_all()
