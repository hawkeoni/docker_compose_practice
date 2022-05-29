FROM python:3.9.13-bullseye
RUN pip install --upgrade pip wheel
RUN pip install tzdata
RUN pip install streamlit==1.9.2 psycopg2-binary==2.9.3
COPY . /ground_truth_updater
WORKDIR /ground_truth_updater
CMD ["streamlit", "run", "main.py"]