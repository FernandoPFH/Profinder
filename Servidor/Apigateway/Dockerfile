FROM python:3.7.8-alpine3.12

RUN pip install "flask==1.1.2"; pip install "pika==1.1.0";

COPY apigateway.py /

CMD ["python", "/apigateway.py"]