from models.models import Categories, Posts


class TestModels:

    def test_categories_as_dict(self):
        cat = Categories(title='Test', ref='test')
        assert cat.as_dict() == {'id': None, 'title': 'Test', 'ref': 'test'}

    def test_posts_as_dict(self):
        post = Posts(title='Test', ref='test', text='some text')
        print(f'{post.as_dict()=}')
        assert post.as_dict() == {'id': None, 'title': 'Test', 'ref': 'test',
                                  'text': 'some text', 'date': 'None', 'date_full': 'None'}
