
pipeline {
    agent { docker { image 'python:3.5.1' } }
    environment {
        BACKENDPATH = "backend/ManagementSystem/"
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'                
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install -r requirements.txt
                    ${BACKENDPATH}/manage.py test ${BACKENDPATH}/Users/tests/"""

            }
        }
    }
}
