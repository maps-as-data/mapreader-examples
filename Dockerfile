# Use an official Python runtime as a parent image
FROM python:3.11

RUN apt-get update

RUN apt-get install -y libgdal-dev libgl1-mesa-glx

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install numpy==1.26.4 torch==2.2.2 torchvision==0.17.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN python -m pip install --no-cache-dir -r requirements.txt

# Clone text spotting repos
RUN git clone https://github.com/maps-as-data/DPText-DETR.git
RUN git clone https://github.com/maps-as-data/DeepSolo.git
RUN git clone https://github.com/maps-as-data/MapTextPipeline.git

# Get text spotting model weights
RUN python -m pip install -U "huggingface_hub[cli]"
RUN huggingface-cli download rwood-97/DPText_DETR_ArT_R_50_poly art_final.pth --local-dir .
RUN huggingface-cli download rwood-97/DeepSolo_ic15_res50 ic15_res50_finetune_synth-tt-mlt-13-15-textocr.pth --local-dir .
RUN huggingface-cli download rwood-97/MapTextPipeline_rumsey rumsey-finetune.pth --local-dir .

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variables
# ENV NAME World

# Run Jupyter Notebook when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
