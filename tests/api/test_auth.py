import os

from flask import session
from flask_blog import app


class TestCategoryApi:
    def setup_method(self):  # Выполняется перед каждым методом
        app.testing = True
        self.client = app.test_client()  # для отправки запросов на сайт

    def test_get(self):
        response = self.client.get('/api/auth')
        assert response.status_code == 200

    def test_post(self):
        with self.client:
            psw = os.getenv('ADMIN_PASS')
            response = self.client.post("/api/auth", json={'name': 'admin', 'psw': psw})
            assert response.status_code == 200
            assert session.get("admin_logged") == 1

            response = self.client.get('/api/auth')
            assert response.json == {'message': f'You logged as admin.'}
