pipeline {
    agent any

    environment {
        MYSQL_ROOT_PASSWORD = 'Basketball01$'
        MYSQL_DATABASE = 'gestor_recetas'
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

        stage('Deploy Database Container') {
            steps {
                script {
                    try {
                        // Levanta solo el contenedor de la base de datos
                        sh 'docker compose up -d db'
                        echo 'Contenedor de la base de datos desplegado exitosamente.'
                    } catch (Exception e) {
                        echo 'Hubo un error al desplegar el contenedor de la base de datos.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Create Database (if necessary)') {
            steps {
                script {
                    try {
                        // Conecta a MySQL para crear la base de datos si no existe
                        sh '''
                            docker exec -t proylm_mysql bash -c "mysql -h 127.0.0.1 -u root -pBasketball01\$ -e 'CREATE DATABASE IF NOT EXISTS gestor_recetas;'"
                        '''
                        echo 'Base de datos creada (o ya existe).'
                    } catch (Exception e) {
                        echo 'Hubo un error al crear la base de datos.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Deploy Backend Container') {
            steps {
                script {
                    try {
                        // Levanta el contenedor de backend después de que la base de datos esté lista
                        sh 'docker compose up -d backend'
                        echo 'Contenedor de backend desplegado exitosamente.'
                    } catch (Exception e) {
                        echo 'Hubo un error al desplegar el contenedor de backend.'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Migrate and Run Django') {
            steps {
                script {
                    try {
                        // Realiza las migraciones de Django
                        sh 'docker exec -i proylm_backend python3 manage.py migrate --noinput'
                        // Recoge archivos estáticos
                        sh 'docker exec -i proylm_backend python3 manage.py collectstatic --noinput'
                        // Inicia el servidor de Django
                        sh 'docker exec -i proylm_backend python3 manage.py runserver 0.0.0.0:8000'
                        echo 'Las migraciones fueron exitosas.'
                    } catch (Exception e) {
                        echo 'Hubo un error con las migraciones de Django.'
                        currentBuild.result = 'FAILURE'
                    }
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
