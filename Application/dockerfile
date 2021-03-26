FROM python:3.8-slim-buster 

WORKDIR /app
COPY ./fastapi-app/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080


CMD ["uvicorn", "api:app", "--host=0.0.0.0", "--port=8080","--reload"]
