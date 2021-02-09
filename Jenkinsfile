
pipeline {
    agent { docker { image 'python:3.5.1' } }
    environment {
        BACKENDPATH = "backend/ManagementSystem/"
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'virtualenv venv'
                sh """
                    source venv/bin/activate
                    pip3 install -r requirements.txt
                """
                sh '${BACKENDPATH}/manage.py test Users/tests/'
            }
        }
    }
}