FROM python:3.9.13-bullseye
RUN pip install --upgrade pip wheel
RUN pip install tzdata
RUN pip install streamlit==1.9.2 psycopg2==2.9.3 \
matplotlib==3.5.2 seaborn==0.11.2 scikit-learn==1.1.1
WORKDIR /dashboard
COPY . /dashboard
CMD ["streamlit", "run", "main.py"]
