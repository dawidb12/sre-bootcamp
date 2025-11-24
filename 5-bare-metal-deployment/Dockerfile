FROM python:3.12-slim-trixie AS builder
ENV PYTHONPATH="/install"
WORKDIR /app
COPY app .
RUN pip3 install --target=/install -r requirements.txt 

FROM python:3.12-slim-trixie AS runner
ENV PYTHONPATH="/usr/local"
ENV DATABASE_URI='postgresql+psycopg2://postgres:postgrespass@flask_db:5432/postgresdb'
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
WORKDIR /app
EXPOSE 5000
CMD sh -c "python3 -m flask db upgrade && python3 -m flask run"