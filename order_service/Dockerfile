# Use the official image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV CONSUL_HOST=consul
ENV PORT=5003

# Make port 5000 available to the world outside this container
EXPOSE 5003

# Define environment variable
ENV FLASK_APP wsgi.py

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "wsgi:app"]
