"""
Описание моделей для базы данных.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # db.init_app(app) - в приложении для подключения ДБ


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    ref = db.Column(db.String(25), unique=True)

    def as_dict(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}

    def __repr__(self):
        return self.title


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    ref = db.Column(db.String(25), unique=True)
    text = db.Column(db.Text)
    date = db.Column(db.Text, default=datetime.utcnow().strftime('%d-%m-%Y'))
    date_full = db.Column(db.DateTime, default=datetime.utcnow())

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship('Categories',
                               backref=db.backref('posts', lazy='dynamic'))

    def as_dict(self):
        res = {item.name: getattr(self, item.name) for item in self.__table__.columns
               if item.name not in ('date', 'category_id', 'category')}
        res.update({'date': str(self.date)})
        res.update({'date_full': str(self.date_full)})
        return res

    def __repr__(self):
        return self.title
