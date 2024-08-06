# Use the official PyTorch image with CUDA support as a parent image
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# Set the working directory
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 3001

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["python3", "app.py"]
