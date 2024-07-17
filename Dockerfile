# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose the port on which Django runs (default is 8000)
EXPOSE 8000

# Command to run Django server within the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
