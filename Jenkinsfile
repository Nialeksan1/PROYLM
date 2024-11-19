pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        DOCKER_HUB_CREDENTIALS = 'docker_hub_credentials' // ID de las credenciales de Docker Hub en Jenkins
        IMAGE_NAME = 'nialeksan1/django-container' // Nombre de la imagen de Docker
    }

    stages {
        stage('Stop and Remove Old Containers') {
            steps {
                script {
                    // Detener y eliminar los contenedores antiguos antes de crear los nuevos
                    sh 'docker compose -f ${DOCKER_COMPOSE_FILE} down --volumes --remove-orphans'
                }
            }
        }

        stage('Clean Checkout Code') {
            steps {
                // Elimina el directorio de trabajo para garantizar un repositorio limpio
                deleteDir() 
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

        stage('Build Docker Images with Docker Compose') {
            steps {
                script {
                    // Solo construir las imágenes, sin ejecutar contenedores
                    sh 'docker compose -f ${DOCKER_COMPOSE_FILE} build'
                    echo 'Las imágenes fueron construidas exitosamente.'
                }
            }
        }


        stage('Wait for MySQL to be Ready') {
            steps {
                script {
                    // Esperar a que MySQL esté listo para aceptar conexiones
                    echo "Waiting for MySQL to be ready..."
                    sleep(time: 20, unit: 'SECONDS')  // Esperar 20 segundos (ajustar según lo necesario)
                }
            }
        }

        stage('Create Database if Not Exists') {
            steps {
                script {
                    def retryCount = 0
                    def maxRetries = 5
                    def success = false
                    
                    while (retryCount < maxRetries && !success) {
                        try {
                            echo "Attempting to create database (Attempt ${retryCount + 1})..."
                            sh 'docker compose exec -T db mysql -u root -p Basketball01$ -e "CREATE DATABASE IF NOT EXISTS gestor_recetas;"'
                            success = true
                        } catch (Exception e) {
                            retryCount++
                            echo "Error while creating database: ${e}"
                            // Esperar 10 segundos antes de intentar de nuevo
                            sleep(time: 10, unit: 'SECONDS')
                        }
                    }
                    
                    if (!success) {
                        error "Failed to create database after ${maxRetries} attempts."
                    }
                }
            }
        }

        stage('Make Migrations') {
            steps {
                script {
                    sh 'docker compose exec -T web python manage.py makemigrations'
                }
            }
        }

        stage('Migrate') {
            steps {
                script {
                    sh 'docker compose exec -T web python manage.py migrate'
                }
            }
        }

        stage('Restart Container') {
            steps {
                script {
                    sh 'docker restart django-container'
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

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    try {
                        // Levanta los contenedores sin reconstruir las imágenes
                        sh 'docker compose -f ${DOCKER_COMPOSE_FILE} up -d'
                        echo 'El entorno fue desplegado exitosamente.'
                    } catch (Exception e) {
                        echo 'Hubo un error al desplegar el entorno con Docker Compose.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
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
