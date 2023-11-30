FROM python:3.9

COPY . /db

WORKDIR /db/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt