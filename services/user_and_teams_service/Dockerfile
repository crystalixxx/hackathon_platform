FROM python:3.12

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#ENV PYTHONPATH=/app

EXPOSE 8000:8000

ENTRYPOINT ["python", "app/main.py"]