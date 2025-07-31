FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY listener.py /app/

CMD ["python3", "listener.py"]