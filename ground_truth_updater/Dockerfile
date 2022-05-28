FROM python:3.8-slim-buster
RUN pip install streamlit psycopg2-binary
COPY . /ground_truth_updater
WORKDIR /ground_truth_updater
CMD ["streamlit", "run", "main.py"]