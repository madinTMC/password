pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myproject:latest'
        CONTAINER_NAME = 'myproject_container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/madinTMC/password.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker run --rm $DOCKER_IMAGE python -m unittest discover -s tests'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh 'docker stop $CONTAINER_NAME || true'
                    sh 'docker rm $CONTAINER_NAME || true'
                    sh 'docker run -d --name $CONTAINER_NAME -p 5000:5000 $DOCKER_IMAGE'
                }
            }
        }
    }
}
