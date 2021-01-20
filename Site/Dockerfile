FROM python:3.7.8-alpine3.12

RUN pip install "flask==1.1.2"; pip install "pika==1.1.0"; pip install "requests==2.25.1"; pip install "pymongo==3.11.2";

COPY MongoDBFuncs.py /

COPY Site.py /

COPY /templates/ /templates/

COPY /static/ /static/

CMD ["python", "/Site.py"]