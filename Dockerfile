FROM python:3.6-slim AS install
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential pkg-config
RUN apt-get install -y python3-markupsafe

FROM install as build
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
RUN ls -alh
EXPOSE 5000
# ENV FLASK_APP=application.py

RUN python manage.py makemigrations explorer


