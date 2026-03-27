pipeline {
    // This tells Jenkins to download a Python image and run the steps inside it
    agent {
        docker { 
            image 'python:3.9-slim' 
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // You must install selenium inside the container before running the script
                sh 'pip install selenium'
            }
        }

        stage('Test') {
            steps {
                // Now 'python3' will be found because it's inside the Python container
                sh 'python3 Basic_test-1.py'
            }
        }
    }

    post {
        success {
            echo 'PASSED: Selenium tests completed successfully.'
        }
        failure {
            echo 'FAILED: Python Selenium tests failed.'
        }
    }
}