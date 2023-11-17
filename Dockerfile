FROM --platform=linux/amd64 python:3.8
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/appVittoria
EXPOSE 8003

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8003"]
