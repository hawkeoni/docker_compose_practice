FROM python:3.8-slim-buster
RUN pip install streamlit psycopg2-binary
COPY . /dashboard
WORKDIR /dashboard
CMD ["streamlit", "run", "main.py"]