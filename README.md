# Flask blog
Блог на Flask, читать могут все, создавать и удалять категории и посты в них доступно только администратору.
Управление сайтом также возможно через API.

При написании приложения использованы следующие основные пакеты: \
[Flask](https://pypi.org/project/Flask/); \
[Flask-SQLAlchemy](https://pypi.org/project/flask-sqlalchemy/); \
[Flask-WTF](https://pypi.org/project/Flask-WTF/); \
[Flask-RESTful](https://pypi.org/project/Flask-RESTful/).

Полный список можно посмотреть в фале 'requirements.txt'.

### Описание Models
> Categories - категории для группировки постов.
>> id - уникальный идентификатор, присваивается автоматически.\
>> title - название категории.\
>> ref - slag для формирования url-адреса (Например 'python'.)

> Posts - посты.
>> id - уникальный идентификатор, присваивается автоматически.\
>> title - название поста.\
>> ref - slag для формирования url-адреса (Например 'pip'.)\
>> text - текст поста, можно писать в формате [Markdown](https://ru.wikipedia.org/wiki/Markdown). \
>> date - дата создания поста в формате '%d-%m-%Y', присваивается автоматически. \
>> date_full - дата создания поста в формате UTC, присваивается автоматически. \
>> category_id - содержит id категории, к которой принадлежит пост.

Так как авторизация доступна всего одному пользователю - администратору, модель для пользователей не создана. 
Для входа под администратором используйте логин - 'admin', пароль задается через переменную окружения 'ADMIN_PASS'.

### Описание API
Всем пользователям доступно чтение постов и категорий. Администратор имеет доступ добавлять и удалять посты и категории.
##### URL: '/api/auth'
* get 
> {'message': 'You logged as admin.'}, status code 200 \
> {'message': 'You are not authorized.'}, status code 200
* post {'name': str, 'psw': str}
> {'message': 'User admin is authorized.'}, status code 200\
> {"error": "Wrong login or password."}, status code 400

##### URL: '/api/categories'
* get
> [ {'id': int, 'title': str, 'ref': str}, {...}, ... ], status code 200 \
> {'message': 'No categories, the base is empty.'}, status code 200
* post {'title': str, 'ref': str}
> {'id': int, 'title': str, 'ref': str}, status code 200 \
> {"error": "You are not authorized."}, status code 401 \
> {"error": "Error adding category."}, status code 400
* delete {'ref': str}
> '', status code 204 \
> {"error": "You are not authorized."}, status code 401 \
> {'error': 'The category have posts.'}, status code 405 \
> {'error': 'The category does not exist.'}, status code 405
##### URL: '/api/categories/<path:category>'
* get
> {'category.title': [ {'id': int, 'title': str, 'ref': str, 'text': str, 'date': str}, {...}, ... ], status code 200 \
> {"error": "The category does not found."}, status code 405
* post {'title': str, 'ref': str, 'text': str}
> {'id': int, 'title': str, 'ref': str, 'text': str, 'date': str}, status code 200 \
> {"error": "You are not authorized."}, status code 401 \
> {"error": "Error adding post."}, status code 400
* delete {'ref': str}
> '', status code 204 \
> {"error": "You are not authorized."}, status code 401 \
> {"error": f"The post '{args['ref']}' does not exist."}, status code 400 \
> {"error": f"The category '{category}' does not exist."}, status code 400

## Установка и запуск

#### Локально на Вашем устройстве
Приложение написано на [Python v.3.11](https://www.python.org). 
1. Скачайте FlaskBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Python](https://www.python.org), если он у Вас еще не установлен.
3. Установите необходимые для работы приложения модули. Для этого откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/FlaskBlog),
выполните команду `pip3 install -r requirements.txt`. Если Вы пользователь Microsoft Windows, то вместо `pip3 install ...` следует использовать  `pip install -r requirements.txt`
4. Установите [переменные окружения](https://wiki.archlinux.org/title/Environment_variables_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)) SECRET_KEY и ADMIN_PASS, например выполнив в терминале 
`export SECRET_KEY="ваш_сложный_секретный_ключ"` и `export ADMIN_PASS=ваш_сложный_пароль_администратора`.
5. Для запуска приложения локально на Вашем устройстве выполните команду `python3 flask_blog.py` (Для Microsoft Windows `python flask_blog.py`).
6. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:5000/
#### В контейнере Docker
1. Скачайте FlaskBlog на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив).
2. Установите [Docker](https://www.docker.com/), если он у Вас еще не установлен.
3. Откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/FlaskBlog).
4. В Dockerfile замените "ваш_сложный_секретный_ключ" и "ваш_сложный_пароль_администратора".
5. Выполните сборку Docker образа (image) `docker build -t flask_blog .`.
6. Запустите контейнер `docker run -p 5000:5000 -d flask_blog`.
7. Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1:5000/