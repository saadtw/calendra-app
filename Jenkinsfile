pipeline {
    agent any
    
    environment {
        DOCKER_HUB_REPO = 'saadtw/calendra-app'
        DOCKER_HUB_CREDENTIALS = 'dockerhub-credentials'
        IMAGE_TAG = "${BUILD_NUMBER}"
        // Environment variables for build - using placeholder values
        // For production, add these as Jenkins credentials
        DATABASE_URL = 'postgresql://postgres:postgres@database:5432/calendra'
        NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = ''
        CLERK_SECRET_KEY = ''
        GOOGLE_OAUTH_CLIENT_ID = ''
        GOOGLE_OAUTH_CLIENT_SECRET = ''
        GOOGLE_OAUTH_REDIRECT_URL = 'http://localhost:3000/api/oauth/callback'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'npm ci'
            }
        }
        
        stage('Lint') {
            steps {
                echo 'Running linter...'
                bat 'npm run lint'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image with docker-compose...'
                script {
                    // Build using docker-compose which handles build args
                    bat 'docker-compose build'
                    
                    // Tag the built image for Docker Hub
                    bat "docker tag calendra-app ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                    bat "docker tag calendra-app ${DOCKER_HUB_REPO}:latest"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_HUB_CREDENTIALS) {
                        bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                        bat "docker push ${DOCKER_HUB_REPO}:latest"
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo 'Deployment stage - Will deploy to Kubernetes in Section C'
                // Kubernetes deployment will be added in Section C
                // Example: bat 'kubectl apply -f k8s/deployment.yaml'
            }
        }
    }
    
    post {
        always {
            script {
                echo 'Cleaning up...'
                // Cleanup commands - ignore errors if they fail
                bat 'docker-compose down -v 2>nul || echo Cleanup attempted'
                bat 'docker system prune -f 2>nul || echo Prune attempted'
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check the logs above.'
        }
    }
}