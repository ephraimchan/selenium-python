pipeline {
    agent {
    docker { image 'python:3.12-slim' }
  }
    
    environment {
        SELENIUM_HUB_URL = 'http://selenium-hub:4444'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                  python -m pip install --upgrade pip setuptools wheel || true
                  python -m pip install selenium pytest
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python Basic_test-1.py'
            }
        }
    }
    
    post {
        always {
            echo 'Test execution completed'
        }
        failure {
            echo 'Tests failed - check Selenium Grid connection'
        }
    }
}