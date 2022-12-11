from models.models import Categories, Posts


class TestModels:

    def test_categories_as_dict(self):
        cat = Categories(title='Debian', ref='debian')
        assert cat.as_dict() == {'id': None, 'title': 'Debian', 'ref': 'debian'}

    def test_posts_as_dict(self):
        post = Posts(title='Debian', ref='debian', text='some text')
        print(f'{post.as_dict()=}')
        assert post.as_dict() == {'id': None, 'title': 'Debian', 'ref': 'debian', 'text': 'some text', 'date': 'None'}
