FROM python:3.8

EXPOSE 8080

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    python -m spacy download en_core_web_lg

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./dashboard .

CMD ["gunicorn", "--workers","4", "--threads", "2", "-b", "0.0.0.0:8080", "wsgi:server"]
