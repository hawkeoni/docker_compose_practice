FROM python:3.9.13-bullseye
RUN pip install --upgrade pip wheel
RUN pip install tzdata
RUN pip install streamlit==1.9.2 requests==2.27.1
WORKDIR /classifier
COPY . /classifier
CMD ["streamlit", "run", "main.py"]