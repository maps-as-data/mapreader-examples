# MapReader Examples

A containerised application for testing out the MapReader library.

## Creating the Docker image

Clone the repository and navigate to the root directory of the repository.

```bash
git clone https://github.com/Living-with-machines/MapReader-examples
cd MapReader-examples
```

To create the Docker image, run the following command:

```bash
docker build -t mapreader-examples .
```

Note: This will take a while to complete as the following activities complete:

- Python setup ~22s
- pip install ~7min
- Downloading maps from NLS ~22-28min
- **Total: ~30-35min**

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