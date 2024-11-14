pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'docker_hub_credentials' // ID de las credenciales de Docker Hub en Jenkins
        IMAGE_NAME = 'nialeksan1/proylm-backend' // Nombre de la imagen de Docker
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clona el repositorio desde la rama 'master'
                git branch: 'master', url: 'https://github.com/Nialeksan1/PROYLM.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Construye la imagen de Docker con la etiqueta 'latest'
                    sh 'docker build -t $IMAGE_NAME:latest .'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Autentica en Docker Hub usando las credenciales configuradas en Jenkins
                    docker.withRegistry('', DOCKER_HUB_CREDENTIALS) {
                        // Hace push de la imagen
                        sh 'docker push $IMAGE_NAME:latest'
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    // Levanta el entorno completo usando docker-compose
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'La imagen de Docker ha sido construida, enviada a Docker Hub y el entorno ha sido desplegado correctamente.'
        }
        failure {
            echo 'Hubo un problema durante el proceso de build, push o deploy.'
        }
    }
}
