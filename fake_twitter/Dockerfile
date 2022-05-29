FROM python:3.9.13-bullseye
RUN pip install --upgrade pip wheel
RUN pip install tzdata
COPY . /fake_twitter
WORKDIR /fake_twitter
CMD ["python", "main.py"]