FROM python:3.12

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

COPY tools/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/app

EXPOSE 8000:8000

CMD ["python", "app/main.py"]