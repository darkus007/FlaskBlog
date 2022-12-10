"""
Блог о web разработке на Flask.
"""
import sqlite3
from os import getenv

from flask import Flask, render_template, url_for, request, flash, redirect
import markdown

from utils.wt_forms import CategoryForm, PostForm
from utils.sqlacchemy_models import db, Categories, Posts
from admin.admin import admin
from api.api import api_bp, api


app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api.init_app(app)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')


# @app.route('/')
# def index():
    # categories = Categories.query.all()
    # return render_template('base.html', categories=categories)


@app.route('/add-category', methods=['POST', 'GET'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Categories(title=form.title.data, ref=form.ref.data)
        try:
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('get_category'))
        except sqlite3.Error:
            db.session.rollback()  # откатываем все изменения
            flash('Ошибка записи в базу данных', 'Error')
    return render_template('add_category.html', form=form, categories=Categories.query.all())


@app.route('/add-post', methods=['POST', 'GET'])
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
            print(f'{cat.ref=} \t {post.ref=}')
            return redirect(url_for('get_post', category=cat.ref, post=post.ref))
        except sqlite3.Error:
            db.session.rollback()  # откатываем все изменения
            flash('Ошибка записи в базу данных', 'Error')
    return render_template('add_post.html', form=form, categories=Categories.query.all())


@app.route('/')
@app.route('/<path:category>')
def get_category(category=None):
    cat = Categories.query.filter_by(ref=category).first()
    if cat is None:
        cat = Categories.query.get(1)
    posts = Posts.query.filter_by(category_id=cat.id).all()
    return render_template('category.html', posts=posts, cat=cat, categories=Categories.query.all())


@app.route('/<path:category>/<path:post>')
def get_post(category, post):
    cat = Categories.query.filter_by(ref=category).first()
    posts = Posts.query.filter_by(category_id=cat.id).all()
    return render_template('post.html', posts=posts, current_post=post, cat=cat, categories=Categories.query.all())


if __name__ == '__main__':
    app.run(debug=True)

    # создаем базу данных и таблицы в ней
    # with app.app_context():
    #     db.create_all()
