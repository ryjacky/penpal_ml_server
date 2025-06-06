# Use the official Python image from the Docker Hub
FROM python:3.12-slim
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY ./app .

# Expose the port that the FastAPI application runs on
EXPOSE 8000

# Run the main application file using Uvicorn
CMD ["fastapi", "run"]