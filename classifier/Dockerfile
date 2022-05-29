FROM python:3.9.13-bullseye
RUN pip install --upgrade pip wheel
RUN pip install tzdata
RUN pip install flask==2.1.2 psycopg2-binary==2.9.3 scikit-learn==1.1.1
WORKDIR /classifier
COPY . /classifier
CMD ["python", "main.py"]