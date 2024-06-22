FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nginx \
    && apt-get clean
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Migrations and collectstatic
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# NGINX configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["python", "manage.py", "runserver" ]