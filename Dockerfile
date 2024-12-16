# Use an official Python base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy Conda environment file to the container
COPY environment.yml /app/environment.yml
COPY stepReader.py /app/stepReader.py
COPY main.py /app/main.py
COPY dxfReader.py /app/dxfReader.py
COPY stlReader.py /app/stlReader.py
COPY svgReader.py /app/svgReader.py
COPY svgReader2.py /app/svgReader2.py

# Create Conda environment and activate it
RUN conda env create -f environment.yml
RUN conda clean -afy

# Activate the Conda environment
SHELL ["conda", "run", "-n", "occenv311", "/bin/bash", "-c"]

# Set the default command
CMD ["python", "main.py"]
