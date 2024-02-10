FROM python:3.11

# Set the working directory
WORKDIR /app

COPY requirements.txt /app

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python", "app.py"]