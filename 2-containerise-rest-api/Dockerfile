FROM python:3.12-slim-trixie
ENV DATABASE_URI='sqlite:///data.db'

WORKDIR /app
COPY app .
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt && \
    flask db init && \
	flask db migrate -m "Create student table" && \
	flask db upgrade

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]