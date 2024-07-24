# MapReader Examples

A containerised application for testing out the MapReader library.

## Creating the Docker image

To create the Docker image, run the following command:

```bash
docker build -t mapreader-examples .
```

Note: This will take a while to complete as maps will be downloaded from the
NLS. In our current tests, it takes ~30-35 minutes to complete.

## Running the Docker container

To run the Docker container, run the following command:

```bash
docker run -p 8888:8888 mapreader-examples
```

## Running the Docker container from Docker Hub

To run the Docker container from Docker Hub, run the following command:

```bash
docker run -p 8888:8888 kallewesterling/mapreader-examples
```
