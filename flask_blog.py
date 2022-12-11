"""
Блог о web разработке на Flask.
"""
from os import getenv

from flask import Flask, render_template

from models.models import db, Categories, Posts
from admin.admin import admin
from api.api import api_bp, api


app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_BINDS'] = {'test': 'sqlite:///test_database.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api.init_app(app)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')


# @app.route('/')
# def index():
    # categories = Categories.query.all()
    # return render_template('base.html', categories=categories)

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
