## First use

All you need to do is to build the docker image and run the container based on that image.

1. Build the image:

```sh
make build_image IMAGE_VERSION=v.1.0.0
```

2. Run the container:

```sh
make run_container IMAGE_VERSION=v.1.0.0
```

While running the make command, do not forget about setting the variable IMAGE_VERSION. You can define it as you like, but remember to refer to the image version that exists in the repository when running the container!