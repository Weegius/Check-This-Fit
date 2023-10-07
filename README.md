# Flask Clothes App

Welcome to the Flask Clothes App, a web application that allows you to manage and showcase your clothing items. This README provides detailed instructions on how to set up and run the application.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/flask-clothes-app.git
   cd flask-clothes-app


## Running with Docker

1. Build the Docker image:

   ```bash
   docker build -t flask-clothes-app .
   ```
2. Run the Docker container:

   ```bash
    docker run -p 5000:5000 flask-clothes-app
    ```
3. Open your browser and go to http://localhost:5000 to view the app.

## Environment Variables
DB_url = database url
skey = secret key
pub_key = public key
