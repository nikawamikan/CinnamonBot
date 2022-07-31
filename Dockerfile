FROM python:3.10.5-alpine3.16
WORKDIR /usr/src/bot
COPY requirements.txt ./
COPY ./dmain.py ./
RUN pip install --no-cache-dir -r requirements.txt