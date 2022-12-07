"""
Описание моделей для базы данных.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()    # db.init_app(app) - в приложении для подключения ДБ


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
