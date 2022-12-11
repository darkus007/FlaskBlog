from flask_blog import app


class TestViews:

    def setup_method(self):    # Выполняется перед каждым тестом
        app.testing = True
        self.client = app.test_client()     # через него может отправлять различные запросы на сайт

    def teardown_method(self):     # Выполняется после каждого теста
        print('Выполняется после каждого теста.')

    def test_index_page(self):
        responce = self.client.get('/')
        assert responce.status_code == 200

# python3 -m pytest -v
