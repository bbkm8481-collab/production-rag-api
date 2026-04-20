pipeline {
    agent any

    environment {
        // Define our image name
        IMAGE_NAME = "mlops-rag-api"
        IMAGE_TAG = "v${env.BUILD_ID}" // Automatically tags with the Jenkins build number
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
