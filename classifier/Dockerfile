FROM python:3.8-slim-buster
RUN pip install flask==2.1.2 psycopg2-binary==2.9.3 scikit-learn==1.1.1
WORKDIR /classifier
COPY . /classifier
CMD ["python", "main.py"]