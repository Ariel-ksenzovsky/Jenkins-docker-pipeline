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


        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh '''
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:latest .
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER} .
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:0.0.${BUILD_NUMBER}
                    '''
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
