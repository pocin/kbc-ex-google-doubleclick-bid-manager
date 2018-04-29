FROM python:3.6-alpine

WORKDIR /code
RUN mkdir -p /data/in/tables/ /data/out/tables
RUN pip install --no-cache-dir --ignore-installed  \
    pytest \
    requests \
    https://github.com/keboola/python-docker-application/zipball/master \
    ijson \
    voluptuous

COPY . /code/

# Run the application
CMD python3 -u /code/main.py
