from flask_blog import app


class TestViews:

    def setup_method(self):  # Выполняется перед каждым тестом
        app.testing = True
        self.client = app.test_client()  # через него может отправлять различные запросы на сайт

    # проверка перенаправления не авторизованного пользователя
    def test_add_category_get(self):
        responce = self.client.get('/admin/add-category')
        assert responce.status_code == 302

    def test_add_category_post(self):
        responce = self.client.post('/admin/add-category')
        assert responce.status_code == 302

    def test_add_post_get(self):
        responce = self.client.get('/admin/add-post')
        assert responce.status_code == 302

    def test_add_post_post(self):
        responce = self.client.post('/admin/add-post')
        assert responce.status_code == 302

# python3 -m pytest -v
