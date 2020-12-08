FROM python:3.7.8-alpine3.12

RUN pip install "pika==1.1.0"; pip install "mysql-connector==2.2.9";

COPY getuserssideinfos.py /

CMD ["python", "/getuserssideinfos.py"]