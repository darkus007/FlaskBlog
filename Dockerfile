# syntax=docker/dockerfile:1
FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV SECRET_KEY="ваш_сложный_секретный_ключ"
ENV ADMIN_PASS="ваш_сложный_пароль_администратора"

EXPOSE 5000

CMD [ "python", "./flask_blog.py" ]
