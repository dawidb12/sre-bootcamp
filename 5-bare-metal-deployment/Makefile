IMAGE_VERSION ?= $(error You didn't specify a value for IMAGE_VERSION! Specify it in the make command, e.g. make <function> "IMAGE_VERSION=1.0.0")

run_tests: run_prerequisites
	cd app/ && \
	python3 -m pytest -v && \
	rm -r .pytest_cache __pycache__

run_lint: run_prerequisites
	python3 -m pylint -E app/*.py && \
	if [ $$? -eq 0 ]; then \
		echo "No errors in the code!"; \
	fi

run_prerequisites:
	touch app/.env
	echo "DATABASE_URI=sqlite:///data.db" > app/.env
	pip3 install -r app/requirements.txt --break-system-packages

prepare_db: run_prerequisites
	if [ -d app/migrations ] && [ -d app/instance ]; then \
		echo "Database already migrated!"; \
	else \
		cd app/ && \
		python3 -m flask db init && \
		python3 -m flask db migrate -m "Create student table" && \
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
	docker compose up -d flask_app1 flask_app2

run_everything: run_db_container run_app_container start_compose

start_compose:
	docker compose up -d

stop_compose:
	docker compose down

delete_everything:
	rm -r app/__pycache__ app/migrations app/instance app/*.log
	docker compose down -v
	docker rmi motov547/student-api:$(IMAGE_VERSION)