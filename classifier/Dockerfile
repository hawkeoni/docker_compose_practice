FROM python:3.8-slim-buster
RUN pip install flask psycopg2-binary sqlalchemy Flask-SQLAlchemy
WORKDIR /classifier
COPY . /classifier
CMD ["python", "main.py"]