"""
Блог о web разработке на Flask.
"""

import os.path

from flask import Flask, render_template, redirect, url_for, Response

from models.models import db, Categories, Posts
from admin.admin import admin
from api.api import api_bp, api
from config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
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


@app.route('/')
@app.route('/<path:category>')
def get_category(category=None) -> str:
    cat = Categories.query.filter_by(ref=category).first()
    if not cat:
        cat = Categories.query.get(1)
        if not cat:
            return render_template('category.html', posts=[], cat=None, categories=[])
    posts = Posts.query.filter_by(category_id=cat.id).all()
    return render_template('category.html', posts=posts, cat=cat, categories=Categories.query.all())


@app.route('/<path:category>/<path:post>')
def get_post(category: str, post: str) -> str | Response:
    cat = Categories.query.filter_by(ref=category).first()
    if cat:
        posts = Posts.query.filter_by(category_id=cat.id).all()
        return render_template('post.html', posts=posts, current_post=post, cat=cat, categories=Categories.query.all())
    return redirect(url_for('get_category'))


if __name__ == '__main__':

    if not os.path.exists('instance/database.db'):
        with app.app_context():
            db.create_all()  # создаем базу данных и таблицы в ней

    app.run(host="0.0.0.0", debug=True, port=5000)      # ssl_context='adhoc' - для переключения на https
