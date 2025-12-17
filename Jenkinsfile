pipeline {
    agent any
    
    environment {
        DOCKER_HUB_REPO = 'saadtw/calendra-app'
        DOCKER_HUB_CREDENTIALS = 'dockerhub-credentials'
        IMAGE_TAG = "${BUILD_NUMBER}"
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
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image with docker-compose...'
                script {
                    // Load credentials and create .env file
                    withCredentials([
                        string(credentialsId: 'calendra-database-url', variable: 'DATABASE_URL'),
                        string(credentialsId: 'clerk-publishable-key', variable: 'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY'),
                        string(credentialsId: 'clerk-secret-key', variable: 'CLERK_SECRET_KEY'),
                        string(credentialsId: 'google-oauth-client-id', variable: 'GOOGLE_OAUTH_CLIENT_ID'),
                        string(credentialsId: 'google-oauth-client-secret', variable: 'GOOGLE_OAUTH_CLIENT_SECRET')
                    ]) {
                        // Create .env file with credentials for docker-compose
                        bat """
                            @echo off
                            echo DATABASE_URL=%DATABASE_URL%> .env
                            echo NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=%NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY%>> .env
                            echo CLERK_SECRET_KEY=%CLERK_SECRET_KEY%>> .env
                            echo GOOGLE_OAUTH_CLIENT_ID=%GOOGLE_OAUTH_CLIENT_ID%>> .env
                            echo GOOGLE_OAUTH_CLIENT_SECRET=%GOOGLE_OAUTH_CLIENT_SECRET%>> .env
                            echo GOOGLE_OAUTH_REDIRECT_URL=%GOOGLE_OAUTH_REDIRECT_URL%>> .env
                        """
                        
                        // Build using docker-compose which handles build args
                        bat 'docker-compose build'
                    }
                    
                    // Tag the built image for Docker Hub
                    bat "docker tag calendra-app-pipeline-app ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                    bat "docker tag calendra-app-pipeline-app ${DOCKER_HUB_REPO}:latest"
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