# Stage 1: Use Miniconda to install pythonocc-core
FROM continuumio/miniconda3 AS builder

# Set WORKDIR and copy conda environment yml
WORKDIR /app
COPY occenv311.yml /app/occenv311.yml

# Create conda env
RUN conda env create -f occenv311.yml

# Activate conda env
SHELL ["conda", "run", "-n", "occenv311", "/bin/bash", "-c"]

# Install dependencies and run cleanup
RUN conda install -c conda-forge pythonocc-core=7.8.1 -y && \
    pip install ezdxf requests && \
    conda clean -afy

# Stage 2: Use a minimal Python image
FROM python:3.11-slim

ENV LD_LIBRARY_PATH="/usr/local/lib"

# Copy the necessary libraries from Miniconda environment 
RUN pip install setuptools --upgrade
COPY --from=builder /opt/conda/envs/occenv311/lib /usr/local/lib

# Copy Python scripts
WORKDIR /app
COPY ./exampleFiles/example.stp .
COPY stepReader.py .
COPY main.py .
COPY dxfReader.py .
COPY svgReader2.py .

# Default command
ENTRYPOINT ["python", "main.py"]
