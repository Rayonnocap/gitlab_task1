FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

RUN useradd -m appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
