FROM python:3.8-slim-buster
RUN pip install streamlit==1.9.2 requests==2.27.1
WORKDIR /classifier
COPY . /classifier
CMD ["streamlit", "run", "main.py"]