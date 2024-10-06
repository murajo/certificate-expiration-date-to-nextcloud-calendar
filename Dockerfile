FROM python:3.12

WORKDIR /app

COPY config.yaml .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "./src/main.py"]