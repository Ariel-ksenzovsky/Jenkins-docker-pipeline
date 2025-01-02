pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'arielk2511'
        DOCKER_TOKEN_ID = 'docker-hub-token'  // Fetch Docker Hub credentials directly here
        DOCKER_IMAGE = 'weather-app'
        GITHUB_REPO = 'Ariel-ksenzovsky/mini-project'
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
                    def build_number = "${env.BUILD_NUMBER}"
                    def version_tag = "0.0.${build_number}"
                    def image_tag_latest = "latest"
                    
                    // Build Docker image with tags
                    sh """
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${version_tag} -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${image_tag_latest} .
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

        stage('Build and Push Docker Image') {
            steps {
                script {
                    sh '''
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${image_tag_latest} .
                    docker build -t ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${version_tag} .
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${image_tag_latest}
                    docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${version_tag}
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
