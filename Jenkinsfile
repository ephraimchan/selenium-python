pipeline {
    agent any
    
    environment {
        SELENIUM_HUB_URL = 'http://selenium-hub:4444'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install selenium pytest'
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