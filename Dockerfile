# syntax=docker/dockerfile:1
FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV SECRET_KEY="your_app_secret_key"
ENV ADMIN_PASS=your_secter_admin_password

EXPOSE 5000

CMD [ "python", "./flask_blog.py" ]
