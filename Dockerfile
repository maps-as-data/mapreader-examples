# Use an official Python runtime as a parent image
FROM python:3.9

RUN apt-get update

RUN apt-get install -y libgdal-dev

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download all maps for example notebooks
RUN python download-examples.py

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variables
# ENV NAME World

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
