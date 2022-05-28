FROM python:3.8-slim-buster
RUN pip install streamlit psycopg2-binary matplotlib seaborn scikit-learn
WORKDIR /dashboard
COPY . /dashboard
CMD ["streamlit", "run", "main.py"]
