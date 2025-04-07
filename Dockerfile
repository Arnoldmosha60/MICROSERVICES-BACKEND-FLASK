FROM python:3.12.7
ENV PYTHONNUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app

ENV FLASK_APP=manager.py  
ENV FLASK_ENV=development  