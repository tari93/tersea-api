FROM python:3.9.20-bullseye

WORKDIR /app

COPY ./src /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "fastapi", "dev", "main.py", "--host", "0.0.0.0" ]
