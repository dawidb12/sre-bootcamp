## First use

1. Before you start with testing the application, you need to ensure that docker, docker compose and make are installed. If not, run below script:

```sh
./prepare_env.sh
```

This will install all needed apps.

2. Run DB migrations:

```sh
make prepare_db
```

3. Run the database container:

```sh
make run_db_container
```

4. Run the flask application container:

```sh
make run_app_container
```

## All-in-one

1. If you want to run everything in correct order (without the preparation script), you can use one command:

```sh
make run_everything
```

## Starting/stopping the stack

1. To start the whole compose, run:

```sh
make start_compose
```

2. To stop the whole compose, run:

```sh
make stop_compose
```

## Cleanup

1. If you would like to cleanup the environment, run below command:

```sh
make delete_everything
```

This will stop and remove all containers, images (db + app) + volumes and database data created during the DB migrations.

While running this make command, do not forget about setting the variable IMAGE_VERSION. Remember to refer to the flask app image version that exists in the repository!

## Testing

1. To run the application tests (you can run them whenever you want), run:

```sh
make run_tests
```