# Voiro Microservices Task

This project consists of two services, `user_service` and `profile_service`, running together using Docker Compose. Follow the steps below to set up and run the project.

## API Documentation
https://documenter.getpostman.com/view/36437082/2sA3e1BVVz

## Prerequisites
 
Before running the project, ensure you have the following installed:

- **Docker**: You can download Docker from [here](https://docs.docker.com/get-docker/).
- **Docker Compose**: Docker Compose is included with Docker Desktop for Windows and Mac. For Linux, you can install it from [here](https://docs.docker.com/compose/install/).
- **Docker Account**: Create a Docker account if you don't have one. Sign up [here](https://hub.docker.com/signup).

## Getting Started

### 1: Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/antinolabs/voiro_task.git
cd voiro_task
```

### Step 2: Docker Login

Log in to your Docker account using the command line:

```sh
sudo docker login
```

### Step 3: Run Application

Run application using the command line:

```sh
sudo docker-compose up
```