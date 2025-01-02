# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the application
EXPOSE 5000

# Run the weather-app.py Python script
CMD ["python", "weather-app.py"]
