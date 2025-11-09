build_image:
	docker build --tag student-api:$(IMAGE_VERSION) .

run_container:
	docker run --env-file .env -d -p 5000:5000 student-api:$(IMAGE_VERSION)