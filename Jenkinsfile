
pipeline {
    agent { docker { image 'python:3.9' } }
    environment {
        BACKENDPATH = "backend/ManagementSystem/"
        SECRET_KEY = credentials('SECRET_KEY')
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                    ${BACKENDPATH}/manage.py test ${BACKENDPATH}/Users/tests/"""

            }
        }
    }
}
