dependencies:
	pip3 install -r requirements.txt --break-system-packages

migrate:
	flask db init
	flask db migrate -m "Create student table"
	flask db upgrade

run_server:
	flask run

run_tests:
	pytest -v