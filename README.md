# Jenkins Docker Pipeline

This repository demonstrates how to set up a Jenkins pipeline to build, test, and deploy a Dockerized application.

## Prerequisites

Before setting up the pipeline, ensure you have the following installed:
- **Jenkins** (with Docker and Pipeline plugins)
- **Docker** (and Docker Compose if required)
- **Git**
- **A GitHub repository** (this repo)

## Setup Instructions

### 1. Install Jenkins and Required Plugins
Ensure Jenkins is installed and running. Install the following plugins:
- **Pipeline**
- **Docker Pipeline**
- **Git**

### 2. Configure Jenkins
- Add credentials for DockerHub (if pushing images)
- Configure a Jenkins agent with Docker installed (if not running Jenkins inside Docker)
- Set up a new **Pipeline Job**

### 3. Define the Jenkins Pipeline
This repository contains a `Jenkinsfile` defining the CI/CD process:
- **Clone the repository**
- **Build the Docker image**
- **Run tests** (if applicable)
- **Push the image to DockerHub** (if configured)
- **Deploy the application** (optional, using Kubernetes or Docker Compose)

### 4. Running the Pipeline
1. Navigate to Jenkins dashboard
2. Create a new **Pipeline Job**
3. Set the repository URL
4. Run the pipeline

## Folder Structure
```
Jenkins-docker-pipeline/
│── Dockerfile         # Defines the containerized application
│── Jenkinsfile        # Defines the CI/CD pipeline
│── src/               # Application source code (if applicable)
│── tests/             # Test scripts (if applicable)
│── README.md          # Project documentation
```

## Environment Variables
If required, configure the following environment variables in Jenkins:
```bash
DOCKERHUB_USERNAME=<your_dockerhub_username>
DOCKERHUB_PASSWORD=<your_dockerhub_password>
IMAGE_NAME=<your_image_name>
```

## Contributing
Feel free to open issues or submit pull requests to improve this pipeline.

## License
This project is licensed under the MIT License.
