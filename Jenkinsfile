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
                sh """#!/bin/bash
                    if [ ! -x venv/bin/activate ]; then
                        python3 -m venv venv
                    fi

                    . venv/bin/activate

                    if [ -e requirements.txt ] && [ ! -n \$(diff <(sort requirements.txt) <(pip3 freeze | sort)) ]; then
                            pip3 install --upgrade pip && pip3 install -r requirements.txt
                    fi

                    ${BACKENDPATH}/manage.py test ${BACKENDPATH}/Users/tests/"""
            }
        }
    }
}
