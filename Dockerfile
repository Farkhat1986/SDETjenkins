# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Allure CLI (опционально, если генерируете отчёт вручную)
RUN apt-get update && apt-get install -y openjdk-11-jre && rm -rf /var/lib/apt/lists/*
RUN curl -o allure.tgz https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.tgz && \
    tar -zxvf allure.tgz -C /opt && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/local/bin/allure && \
    rm allure.tgz

COPY . .

# По умолчанию — ничего не запускаем, но можно указать CMD
CMD ["python", "--version"]
