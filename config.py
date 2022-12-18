"""
Модуль содержит настройки проекта.

LOGIN - логин администратора, которому доступно редактирование постов и категорий.
PASSWORD - пароль администратора.

SECRET_KEY - секретный ключ для обеспечения безопасности сессий.
"""

from os import getenv

LOGIN = 'admin'
PASSWORD = getenv('ADMIN_PASS')
SECRET_KEY = getenv('SECRET_KEY')
