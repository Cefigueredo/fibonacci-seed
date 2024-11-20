# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# Copy the FastAPI app code into the container
COPY ./app /app

# Expose the port the app runs on
EXPOSE 8000

WORKDIR /

# Command to run the FastAPI app using Uvicorn
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
