from flask_blog import app


class TestCategoriesAuthApi:

    def setup_method(self):  # Выполняется перед каждым тестом
        app.testing = True
        self.client = app.test_client()  # для отправки запросов на сайт
        with self.client.session_transaction() as session:
            session['admin_logged'] = 1

    def teardown_method(self):
        self.client.delete('http://127.0.0.1:5000/api/categories',
                           json={'ref': 'test_test'})

    def test_get(self):
        response = self.client.get('/api/categories')
        assert response.status_code == 200

    def test_post(self):
        response = self.client.post('http://127.0.0.1:5000/api/categories',
                                    json={'title': 'test_Test_test', 'ref': 'test_test'})
        assert response.status_code == 200

    def test_delete(self):
        self.client.post('http://127.0.0.1:5000/api/categories',
                         json={'title': 'test_Test_test', 'ref': 'test_test'})
        response = self.client.delete('http://127.0.0.1:5000/api/categories',
                                      json={'ref': 'test_test'})
        assert response.status_code == 204


class TestCategoriesUnAuthApi:

    def setup_method(self):  # Выполняется перед каждым тестом
        app.testing = True
        self.client = app.test_client()  # для отправки запросов на сайт

    def teardown_method(self):
        with self.client.session_transaction() as session:
            session['admin_logged'] = 1
        self.client.delete('http://127.0.0.1:5000/api/categories',
                           json={'ref': 'test_test'})

    def test_get(self):
        response = self.client.get('/api/categories')
        assert response.status_code == 200

    def test_post(self):
        response = self.client.post('http://127.0.0.1:5000/api/categories',
                                    json={'title': 'test_Test_test', 'ref': 'test_test'})
        assert response.status_code == 401

    def test_delete(self):
        self.client.post('http://127.0.0.1:5000/api/categories',
                         json={'title': 'test_Test_test', 'ref': 'test_test'})
        response = self.client.delete('http://127.0.0.1:5000/api/categories',
                                      json={'ref': 'test_test'})
        assert response.status_code == 401

# python3 -m pytest -v
