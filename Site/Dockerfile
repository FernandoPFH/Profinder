FROM python:3.7.8-alpine3.12

RUN pip install "flask==1.1.2"; pip install "pika==1.1.0"; pip install requests;

COPY Site.py /

COPY /templates/ /templates/

COPY /static/ /static/

COPY /SessionishModule/ /SessionishModule/

COPY /SessionishFiles/ /SessionishFiles/

CMD ["python", "/Site.py"]