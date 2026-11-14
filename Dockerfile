# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use pip cache mount to speed up builds and avoid redownloading packages
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p data

# Expose port 8000 (internal)
EXPOSE 8000

# Define environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Run the command to start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
