## First use

1. To start with this excercise you need to run the following command:

```sh
make dependencies
```

This will install all the respective dependencies to run the Flask webserver.

2. To initiate the database, run:

```sh
make migrate
```

The database is ready and you can run the application.

3. To run the flask webserver, run:

```sh
make run_server
```

If you want to stop the server, press Ctrl + C

4. If you want to run tests only, run:

```sh
make run_tests
```