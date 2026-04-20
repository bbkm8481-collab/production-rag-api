pipeline {
    agent any

    environment {
        IMAGE_NAME = "mlops-rag-api"
        IMAGE_TAG = "v${env.BUILD_ID}"
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to Production') {
            steps {
                echo "Deploying the latest AI container..."
                // 1. Force stop the old container if it exists (|| true prevents errors if it doesn't exist)
                sh "docker rm -f mlops-rag-container || true"
                
                // 2. Run the new container in the background (-d) on port 8000
                sh "docker run -d -p 8000:8000 --name mlops-rag-container ${IMAGE_NAME}:latest"
            }
        }

        stage('Security & Cleanup') {
            steps {
                echo "Cleaning up dangling images to save space..."
                sh "docker system prune -f"
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline Succeeded! The new RAG API is currently LIVE on port 8000."
        }
        failure {
            echo "❌ Pipeline Failed! Please check the logs."
        }
    }
}
