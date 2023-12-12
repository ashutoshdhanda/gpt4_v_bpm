# Use an official Python runtime as a parent image
FROM python:3.11.6-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install git
RUN apt-get update && \
    apt-get install -y git

# Clone the specified git repository
RUN git clone https://github.com/ashutoshdhanda/gpt4_v_bpm.git

# Set the working directory to the app directory
WORKDIR /usr/src/app/gpt4_v_bpm

# Install any needed packages specified in requirements.txt
RUN pip install streamlit

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
