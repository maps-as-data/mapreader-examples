# MapReader Examples

This repo contains worked examples of using the MapReader library for various geospatial and non-geospatial tasks. 

There are two ways to set up and run these worked examples:

1. [Install MapReader on your machine and run the examples locally](#local-install)
2. [Use the Docker container provided in this repo to install MapReader and run the examples in a containerized environment](#docker-container)

## Local install

As per the [MapReader installation instructions](https://mapreader.readthedocs.io/en/latest/getting-started/installation-instructions/index.html), to run these worked examples locally you will need to:

1. Clone the `mapreader-examples` repository
2. Set up a Python virtual environment
3. Install the required dependencies (NOTE: for the worked examples, these are different from those in the MapReader installation instructions!)
4. Add your Python virtual environment to Jupyter Notebook as a kernel
5. Run the worked examples in Jupyter Notebook (or other IDE)

### 1. Clone the `mapreader-examples` repository

To clone the `mapreader-examples` repository, run the following command:

```bash
git clone https://github.com/maps-as-data/mapreader-examples.git
```

This will copy the code and worked examples into your current working directory. 

### 2. Set up a Python virtual environment

If you are using conda, run the following commands to set up a new conda environment:

```bash
conda create -n mapreader_examples python=3.12
conda activate mapreader_examples
```

**Or**, if you want to use venv instead of conda, run the following commands:

```bash
python3 -m venv mapreader_examples
source mapreader_examples/bin/activate
```

### 2. Install the required dependencies

To install the dependencies for the worked examples, run the following commands:

```bash
cd mapreader-examples
pip install -r requirements.txt
```

### 3. Add your Python virtual environment to Jupyter Notebook as a kernel

To allow the newly created Python virtual environment to show up in Jupyter notebooks, run the following command:

```bash
python -m ipykernel install --user --name "mapreader_examples"
```

### 4. Run the worked examples in Jupyter Notebook

Lastly, to open a Jupyter Notebook, run the following command:

```bash
jupyter notebook
```

This will open a Jupyter Notebook in your browser.
If it doesn't open, copy the link shown in your terminal and paste it into a new tab. 
From here, you can navigate to the `notebooks` directory and open the worked examples you are interested in and start running the code.
Any changes you make will be saved locally to your files.

## Docker container

If you have issues with the local install, or would prefer to run the worked examples in a containerized environment, you can use the Docker container provided in this repo.
You will need to have docker installed on your machine to run the container.

### 1. Clone the `mapreader-examples` repository

To clone the `mapreader-examples` repository, run the following command:

```bash
git clone https://github.com/maps-as-data/mapreader-examples.git
```

This will copy the code and worked examples into your current working directory. 

### 2. Build the Docker image

To create the Docker image, run the following command:

```bash
cd mapreader-examples
docker build -t mapreader-examples .
```

Note: This may take a while to complete (approx 10-15 minutes).

### 3. Run the Docker container

To run the Docker container, run the following command:

```bash
docker run -p 8888:8888 mapreader-examples
```

This will start the Jupyter Notebook in the docker container and should pop up in your browser. 
If it doesn't, copy the link provided in the terminal and paste it into a new tab.
From here, you can navigate to the `notebooks` directory and open the worked examples you are interested in and start running the code.
Any changes you make will be saved in the docker container, but won't be saved locally to your files unless you copy them over.

## Docker Hub

If you'd like to use the docker image hosted on Docker Hub, run the following command:

```bash
docker run -p 8888:8888 kallewesterling/mapreader-examples
```
