IMAGE_VERSION ?= $(error Nie podałeś wartości dla IMAGE_VERSION! Podaj ją w komendzie make, np. make <funkcja> "IMAGE_VERSION=1.0.0")

run_tests: run_prerequisites
	cd app/ && \
	pytest -v && \
	rm -r .pytest_cache __pycache__

run_prerequisites:
	touch app/.env
	echo "DATABASE_URI=sqlite:///data.db" > app/.env
	pip3 install -r app/requirements.txt --break-system-packages

prepare_db: run_prerequisites
	if [ -d app/migrations ] && [ -d app/instance ]; then \
		echo "Database already migrated!"; \
	else \
		cd app/ && \
		flask db init && \
		flask db migrate -m "Create student table" && \
		rm .env; \
	fi

run_db_container: prepare_db
	OUTPUT_PS=$$(docker ps --format 'table {{.Names}}' | grep -i flask_db) && \
	if [ -z "$$OUTPUT_PS" ]; then \
		docker compose up -d flask_db; \
	fi; \
	OUTPUT_INSPECT=$$(docker inspect flask_db --format '{{.State.Status}}' 2>/dev/null); \
	if [ "$$OUTPUT_INSPECT" = "running" ]; then \
    	echo "The DB container is running!"; \
	else \
		docker compose up -d flask_db; \
	fi

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
	rm -r app/__pycache__ app/migrations app/instance app/*.log
	docker compose down -v
	docker rmi student-api:$(IMAGE_VERSION)