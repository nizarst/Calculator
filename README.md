

# ➕ FastAPI RPN Calculator ➕


**Description:** This is a simple FastAPI-based Reverse Polish Notation (RPN) calculator API. The API supports basic arithmetic operations and provides endpoints to perform calculations and export database data to a CSV file. The entire solution is dockerized, including the FastAPI application, MySQL database, and phpMyAdmin interface.

**Prerequisites:**
- Docker
- Docker Compose
- Python 3.9+

**Getting Started:**
    
    git clone https://github.com/your_username/fastapi-rpn-calculator.git
    cd fastapi-rpn-calculator

**Set Up Environment Variables**

The .env file should be included in the .gitignore file to avoid exposing sensitive information. However, for the purpose of this exercise, it is included in the repository.

**Build and Run the Docker Containers**

docker-compose up --build


**Access the API**

The FastAPI application will be available at http://localhost:8000.


**Note:**
We can create a docker image and push it to docker hub using this commands:

    docker build -t dockerhub_username/fastapi-rpn-calculator .

When running it locally just type:

    docker run -p 8000:8000 --env-file .env dockerhub_username/fastapi-rpn-calculator

Tag and Push the Docker Image:

    docker push dockerhub_username/fastapi-rpn-calculator:latest

