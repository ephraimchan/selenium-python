pipeline {
    agent any
    
    environment {
        SELENIUM_HUB_URL = 'http://selenium-hub:4444'
    }
    
    stages {
        stage('Setup') {
            steps {
                bat 'pip install selenium pytest'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'python Basic_test-1.py'
            }
        }
    }
}