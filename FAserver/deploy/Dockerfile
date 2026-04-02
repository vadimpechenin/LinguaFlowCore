FROM python:3.11-slim-bookworm
WORKDIR /app
COPY ./deploy/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN rm -f /app/requirements.txt
COPY main/src /app

# Переменные используемые сервисом, не удалять
ENV SENTENCE_TRANSFORMERS_CACHE=/sentence_transformers_cache
ENV HF_HUB_OFFLINE=1
ENV SENTENCE_TRANSFORMERS_HOME=$SENTENCE_TRANSFORMERS_CACHE

#Пути к данным
ARG SENTENCE_TRANSFORMERS_CACHE_SRC=test/resources/sentence_transformers_cache

RUN mkdir $SENTENCE_TRANSFORMERS_CACHE

COPY $SENTENCE_TRANSFORMERS_CACHE_SRC/ $SENTENCE_TRANSFORMERS_CACHE/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]