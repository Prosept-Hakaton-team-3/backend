FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi"]
