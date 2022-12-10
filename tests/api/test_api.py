import requests
from api import app


# res = requests.get('http://127.0.0.1:5000/api/categories')
# print(f'{res}\t{res.json() if res.status_code==200 else ""}')


# res = requests.post('http://127.0.0.1:5000/api/categories', json={'title': 'Debian', 'ref': 'debian'})
# print(f'{res}\t{res.json() if res.status_code==200 else ""}')

# res = requests.delete('http://127.0.0.1:5000/api/categories', json={'ref': 'debian'})
# print(f'{res}\t{res.text}')

# res = requests.post('http://127.0.0.1:5000/api/categories/python',
#                     json={'title': 'Debian', 'ref': 'debian', 'text': 'some text'})
# print(f'{res}\t{res.json() if res.status_code==200 else ""}')
# print(f'{res.text}')

res = requests.delete('http://127.0.0.1:5000/api/categories/python', json={'ref': 'debian'})
print(f'{res}\t{res.text}')
