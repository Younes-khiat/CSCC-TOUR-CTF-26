FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

# Copy the application
COPY app.py .
COPY flag.txt .
COPY file_storage/ file_storage/

EXPOSE 80

CMD ["python", "app.py"]
