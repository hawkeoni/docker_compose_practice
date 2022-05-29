FROM python:3.8-slim-buster
RUN pip install streamlit requests
WORKDIR /classifier
COPY . /classifier
CMD ["streamlit", "run", "main.py"]