FROM mcr.microsoft.com/playwright/python:v1.48.0-focal

ENV FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
