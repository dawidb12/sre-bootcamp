FROM python:3.12-slim-trixie AS builder
ENV DATABASE_URI='sqlite:///data.db'
ENV PYTHONPATH="/install"
WORKDIR /app
COPY app .
RUN pip3 install --target=/install -r requirements.txt 
RUN python -m flask db init && \
	python -m flask db migrate -m "Create student table" && \
	python -m flask db upgrade

FROM python:3.12-slim-trixie AS runner
ENV PYTHONPATH="/usr/local"
ENV DATABASE_URI='sqlite:///data.db'
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run"]