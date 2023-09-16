# Use the official Airflow image as the base image
FROM apache/airflow:latest

# Copy the requirements.txt file to the image
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory back to the original
WORKDIR /opt/airflow