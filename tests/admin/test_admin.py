from flask_blog import app


class TestUnAuthViews:

    def setup_method(self):  # Выполняется перед каждым тестом
        """
        Выполняется перед каждым запросом, создает self.client,
        через которого можно отправлять запросы (get, post, delete ...)
        """
        app.testing = True
        self.client = app.test_client()  # через него может отправлять различные запросы на сайт

    # проверка перенаправления не авторизованного пользователя
    def test_add_category_get(self):
        response = self.client.get('/admin/add-category')
        assert response.status_code == 302

    def test_add_category_get_redirect(self):
        response = self.client.get('/admin/add-category', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/login"

    def test_add_category_post(self):
        response = self.client.post('/admin/add-category')
        assert response.status_code == 302

    def test_add_category_post_redirect(self):
        response = self.client.post('/admin/add-category', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/login"

    def test_add_post_get(self):
        response = self.client.get('/admin/add-post')
        assert response.status_code == 302

    def test_add_post_get_redirect(self):
        response = self.client.get('/admin/add-post', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/login"

    def test_add_post_post(self):
        response = self.client.post('/admin/add-post')
        assert response.status_code == 302

    def test_add_post_post_redirect(self):
        response = self.client.post('/admin/add-post', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/login"


class TestAuthViews:

    def setup_method(self):  # Выполняется перед каждым тестом
        """
        Авторизуем админа минуя форму авторизации,
        установив ключ напрямую в сессию.
        """
        app.testing = True
        self.client = app.test_client()  # через него может отправлять различные запросы на сайт
        with self.client.session_transaction() as session:
            session['admin_logged'] = 1

    def test_add_category(self):
        # отправляем запрос с включенной переадресацией, если админ не авторизован
        # то он будет перенаправлен на страницу авторизации, это и проверяем
        response = self.client.get('/admin/add-category', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/add-category"

    def test_add_post(self):
        response = self.client.get('/admin/add-post', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin/add-post"

# python3 -m pytest -v
