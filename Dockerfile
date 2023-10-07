# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 5000 for the Flask application
EXPOSE 5000

# Environment variables 
ENV DB_URL=mongodb://srv-captain--final-db/mydatabase?authSource=admin
ENV SKEY=o1HM3lo7Snqp4gHM@^93e7g%fe&pgEZ#ep
ENV PUB_KEY=12ced8960637e7633241


# Command to run the application
CMD ["python", "app.py"]
