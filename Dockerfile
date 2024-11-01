FROM python:3.10-alpine

RUN apk add git --no-cache

WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
