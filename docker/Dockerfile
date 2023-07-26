FROM python:3.11.4-slim

USER root
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY dependencies.py ./dependencies.py
COPY routers ./routers
COPY main.py ./main.py

CMD ["python", "main.py"]
