FROM python:3.11-slim-bookworm
WORKDIR /app

# Добавляем инструменты сборки и библиотеки для Postgres
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./deploy/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN rm -f /app/requirements.txt
# Специально из за строки nlp = spacy.load("en_core_web_sm")
RUN python -m spacy download en_core_web_sm

COPY app /app/app
COPY weights /app/weights

# Переменные используемые сервисом, не удалять
ENV SENTENCE_TRANSFORMERS_CACHE=/app/weights/sentence_transformers_cache
ENV HF_HUB_OFFLINE=1
ENV SENTENCE_TRANSFORMERS_HOME=$SENTENCE_TRANSFORMERS_CACHE

#Пути к данным
#ARG SENTENCE_TRANSFORMERS_CACHE_SRC=tests/resources/sentence_transformers_cache

#RUN mkdir $SENTENCE_TRANSFORMERS_CACHE

#COPY $SENTENCE_TRANSFORMERS_CACHE_SRC/ $SENTENCE_TRANSFORMERS_CACHE/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]