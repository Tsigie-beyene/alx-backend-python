# Use the official Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app code into the container
COPY . .

# Note: To map the container port to the host, use ["-p"] 8000:8000 in the docker run command, e.g., docker run ["-p"] 8000:8000 messaging_app
# Expose the port the Django app runs on
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1

# Run Django migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
