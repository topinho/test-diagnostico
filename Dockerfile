FROM python:3.9-alpine

WORKDIR /app

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers openssl-dev

COPY app/requirements.txt /app/requirements.txt

RUN pip install PyMySQL

RUN pip install -r requirements.txt

COPY app /app

#EXPOSE 5005

CMD ["flask", "run"]