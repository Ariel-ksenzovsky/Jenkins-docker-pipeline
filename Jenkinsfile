pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'arielk2511'
        DOCKER_TOKEN_ID = 'docker-hub-token'  // Fetch Docker Hub credentials directly here
        DOCKER_IMAGE = 'weather-app'
        GITHUB_REPO = 'Ariel-ksenzovsky/Jenkins-docker-pipeline'
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image with tags
                    sh """
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER} -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests
                    sh """
                    docker run -d -p 5000:5000 ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER}
                    echo "Waiting for application to start..."
                    until curl --fail --max-time 120 http://localhost:5000; do
                        echo "Waiting for application to start..."
                        sleep 5
                    done
                    echo "Application started successfully!"
                    """
                }
            }
        }  

        stage('Create PR to Main') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    // Disable sandbox to allow the curl command
                    sh """
                    curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                    -d '{"title": "Merge feature branch to main", "head": "${env.BRANCH_NAME}", "base": "main"}' \
                    https://api.github.com/repos/${GITHUB_REPO}/pulls
                    """
                }
            }
        }

        stage('Docker Login') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([string(credentialsId: env.DOCKER_TOKEN_ID, variable: 'DOCKER_TOKEN')]) {
                        sh """
                        echo "$DOCKER_TOKEN" | docker login -u arielk2511 --password-stdin
                        """
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh """
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy to instance via terraform') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh """
                    cd terraform
                    terraform init
                    terraform apply -auto-approve
                    """
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh """
                    docker rmi ${DOCKER_USERNAME}/${DOCKER_IMAGE}:latest
                    docker rmi ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER}
                    """
                }
            }
        }
        
    }

    


    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
