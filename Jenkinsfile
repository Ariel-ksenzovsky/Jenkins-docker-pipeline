pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'arielk2511'  // Replace with your Docker Hub username
        DOCKER_PASSWORD = 'docker-hub-token'  // Jenkins Docker Hub credentials
        DOCKER_IMAGE = 'weather-app'
        GITHUB_REPO = 'https://github.com/Ariel-ksenzovsky/mini-project.git'  // Replace with your GitHub repository name (e.g., 'username/repo')
        GITHUB_TOKEN = credentials('github-token')  // GitHub credentials for PR creation
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm  // Checkout the code from the GitHub repository
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

        stage('Push Docker Image') {
            when {
                branch 'main'  // Only push Docker image when on 'main' branch
            }
            steps {
                   withCredentials([string(credentialsId: env.DOCKER_TOKEN_ID, variable: 'DOCKER_TOKEN')]) {
                        sh """
                        echo "$DOCKER_TOKEN" | docker login -u arielk2511 --password-stdin
                        docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${version_tag}
                        docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${image_tag_latest}
                        """
                }
            }
        }

        stage('Create PR to Main') {
            when {
                not {
                    branch 'main'  // Only create PR if the branch is not 'main'
                }
            }
            steps {
                script {
                    // Create a PR using GitHub API (via curl)
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
