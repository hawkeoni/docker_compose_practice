FROM python:3.8-slim-buster
RUN pip install streamlit==1.9.2 psycopg2-binary==2.9.3
COPY . /ground_truth_updater
WORKDIR /ground_truth_updater
CMD ["streamlit", "run", "main.py"]