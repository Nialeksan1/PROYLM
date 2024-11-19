pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'docker_hub_credentials' // ID de las credenciales de Docker Hub en Jenkins
        IMAGE_NAME = 'nialeksan1/proylm-backend' // Nombre de la imagen de Docker
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    try {
                        // Clona el repositorio desde la rama 'master'
                        git branch: 'master', url: 'https://github.com/Nialeksan1/PROYLM.git'
                        echo 'Checkout del código exitoso.'
                    } catch (Exception e) {
                        echo 'Hubo un error al hacer checkout del código.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        // Construye la imagen de Docker con la etiqueta 'latest'
                        sh 'docker build -t $IMAGE_NAME:latest .'
                        echo 'La imagen de Docker fue construida exitosamente.'
                    } catch (Exception e) {
                        echo 'Hubo un error al construir la imagen de Docker.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    try {
                        // Autentica en Docker Hub usando las credenciales configuradas en Jenkins
                        docker.withRegistry('', DOCKER_HUB_CREDENTIALS) {
                            // Hace push de la imagen
                            sh 'docker push $IMAGE_NAME:latest'
                            echo 'La imagen fue enviada exitosamente a Docker Hub.'
                        }
                    } catch (Exception e) {
                        echo 'Hubo un error al hacer push de la imagen a Docker Hub.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        /* stage('Deploy with Docker Compose') {
            steps {
                script {
                    try {
                        // Levanta el entorno completo usando docker-compose
                        sh 'docker compose up -d'
                        echo 'El entorno fue desplegado exitosamente.'
                    } catch (Exception e) {
                        echo 'Hubo un error al desplegar el entorno con Docker Compose.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        } */
    }

    post {
        success {
            echo 'El pipeline se completó exitosamente.'
        }
        failure {
            echo 'Hubo un problema durante la ejecución del pipeline.'
        }
    }
}
