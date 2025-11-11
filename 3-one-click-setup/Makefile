IMAGE_VERSION ?= $(error Nie podałeś wartości dla IMAGE_VERSION! Podaj ją w komendzie make, np. make <funkcja> "IMAGE_VERSION=1.0.0")

run_tests: run_prerequisites
	cd app/ && \
	pytest -v

run_prerequisites:
	touch app/.env
	echo "DATABASE_URI=sqlite:///data.db" > app/.env
	pip3 install -r app/requirements.txt --break-system-packages

prepare_db: run_prerequisites
	cd app/ && \
	flask db init && \
	flask db migrate -m "Create student table" && \
	rm .env

run_db_container: prepare_db
	pwd
	docker compose up -d flask_db

build_app_image:
	docker compose build

run_app_container: build_app_image
	docker compose up -d flask_app

run_everything: run_db_container run_app_container

start_compose:
	docker compose up

stop_compose:
	docker compose down

delete_everything:
	docker compose down -v
	docker rmi student-api:$(IMAGE_VERSION)
	rm -r app/__pycache__ app/migrations app/instance app/*.log