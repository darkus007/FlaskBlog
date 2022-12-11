"""
API для работы с сайтом.
Использована библиотека Flask-RESTful.

Реализовано:
    - чтений всех категорий, добавление категорий, удаление категорий;
    - чтение всех постов в выбранной категории; добавление и удаление поста.

"""


from flask import Blueprint
from models.models import db, Posts, Categories
from flask_restful import reqparse, Api, Resource

api_bp = Blueprint('api', __name__)

api = Api()


class CategoriesApi(Resource):
    def get(self):
        """ Возвращает все имеющиеся категории. """
        cats = Categories.query.all()
        return [cat.as_dict() for cat in cats]

    def post(self):
        """ Добавляет новую категорию. """
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('ref', type=str)
        args = parser.parse_args()
        cat = Categories(title=args["title"], ref=args["ref"])
        try:
            db.session.add(cat)
            db.session.commit()
        except Exception:
            db.session.rollback()
        cat = Categories.query.filter_by(ref=args["ref"]).first()
        return cat.as_dict()

    def delete(self):
        """ Удаляет категорию если в ней нет постов. """
        parser = reqparse.RequestParser()
        parser.add_argument('ref', type=str)
        args = parser.parse_args()
        cat_to_del = Categories.query.filter_by(ref=args['ref']).first()
        if cat_to_del:
            if Posts.query.filter_by(category_id=cat_to_del.id).first():
                return {'error': 'The category have posts.'}, 405
            db.session.delete(cat_to_del)
            db.session.commit()
            return '', 204
        return {'error': 'The category does not exist.'}, 405


class CategoryApi(Resource):
    def get(self, category):
        """ Возвращает все статьи в указанной категории. """
        cat = Categories.query.filter_by(ref=category).first()
        posts = Posts.query.filter_by(category_id=cat.id).all()
        return {cat.title: [post.as_dict() for post in posts]}

    def post(self, category):
        """ Добавляет статью в указанную категорию. """
        cat = Categories.query.filter_by(ref=category).first()
        if cat:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('ref', type=str)
            parser.add_argument('text', type=str)
            args = parser.parse_args()
            post = Posts(title=args['title'], ref=args['ref'], text=args['text'], category_id=cat.id)
            try:
                db.session.add(post)
                db.session.commit()
                return Posts.query.filter_by(ref=args["ref"]).first().as_dict()
            except Exception:
                db.session.rollback()
        return {"error": "Error adding post."}, 400      # Bad Request

    def delete(self, category: str):
        """
        Удаляет пост, если он принадлежит указанной категории (category).
        :param category: Категория, которая содержит удаляемый пост.
        """
        cat = Categories.query.filter_by(ref=category).first()
        if cat:
            parser = reqparse.RequestParser()
            parser.add_argument('ref', type=str)
            args = parser.parse_args()
            post_to_del = Posts.query.filter_by(ref=args['ref']).first()
            if post_to_del:
                if cat.id == post_to_del.category_id:
                    db.session.delete(post_to_del)
                    db.session.commit()
                    return '', 204      # No Content
            else:
                return {"error": f"The post '{args['ref']}' does not exist."}, 400
        return {"error": f"The category '{category}' does not exist."}, 400      # Bad Request


api.add_resource(CategoriesApi, '/api/categories')                  # Возвращает все имеющиеся категории.
api.add_resource(CategoryApi, '/api/categories/<path:category>')    # Возвращает все статьи в указанной категории.
