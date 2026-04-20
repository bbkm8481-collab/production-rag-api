pipeline {
    agent any

    environment {
        IMAGE_NAME = "mlops-rag-api"
        IMAGE_TAG = "v${env.BUILD_ID}"
        // 🔥 PRO FIX: Tell Jenkins to look in Mac's default application folders for Docker
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

        stage('Security & Cleanup') {
            steps {
                echo "Cleaning up dangling images to save space..."
                sh "docker system prune -f"
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline Succeeded! The RAG API is containerized and ready for deployment."
        }
        failure {
            echo "❌ Pipeline Failed! Please check the logs."
        }
    }
}
