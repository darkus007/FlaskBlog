from flask_blog import app


class TestCategoryAuthApi:
    def setup_method(self):  # Выполняется перед каждым методом
        app.testing = True
        self.client = app.test_client()  # для отправки запросов на сайт
        with self.client.session_transaction() as session:
            session['admin_logged'] = 1
        self.client.post('/api/categories',  # метод класса CategoriesApi
                         json={'title': 'test_Test_test', 'ref': 'test_category_test'})

    def teardown_method(self):  # Выполняется после каждого метода
        self.client.delete('/api/categories/test_category_test',
                           json={'ref': 'test_post_test'})
        self.client.delete('/api/categories',  # метод класса CategoriesApi
                           json={'ref': 'test_category_test'})

    def test_get(self):
        response = self.client.get('/api/categories/test_category_test')
        assert response.status_code == 200

    def test_post(self):
        response = self.client.post('/api/categories/test_category_test',
                                    json={'title': 'test_Post_test',
                                          'ref': 'test_post_test',
                                          'text': 'some text'}
                                    )
        assert response.status_code == 200

    def test_delete(self):
        self.client.post('/api/categories/test_category_test',
                         json={'title': 'test_post_test',
                               'ref': 'test_post_test',
                               'text': 'some text'}
                         )

        response = self.client.delete('/api/categories/test_category_test',
                                      json={'ref': 'test_post_test'})
        assert response.status_code == 204


class TestCategoryUnAuthApi:
    def setup_method(self):  # Выполняется перед каждым методом
        app.testing = True
        self.client = app.test_client()  # для отправки запросов на сайт

    def teardown_method(self):  # Выполняется после каждого метода
        with self.client.session_transaction() as session:
            session['admin_logged'] = 1
        self.client.delete('/api/categories',  # метод класса CategoriesApi
                           json={'ref': 'test_category_test'})
        self.client.delete('/api/categories/test_category_test',
                           json={'ref': 'test_post_test'})

    def test_get(self):
        response = self.client.get('/api/categories/test_category_test')
        assert response.status_code == 405

    def test_post(self):
        response = self.client.post('/api/categories/test_category_test',
                                    json={'title': 'Debian', 'ref': 'test_post_test', 'text': 'some text'})
        assert response.status_code == 401

    def test_delete(self):
        self.client.post('/api/categories/test_category_test',
                         json={'title': 'Debian', 'ref': 'test_post_test', 'text': 'some text'})
        response = self.client.delete('/api/categories/test_category_test',
                                      json={'ref': 'test_post_test'})
        assert response.status_code == 401
