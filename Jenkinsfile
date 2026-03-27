pipeline {
    agent any
    stages {
        stage('Install Environment') {
            steps {
                // This installs python if it's missing from the container
                sh 'apt-get update && apt-get install -y python3'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 Basic_test-1.py'
            }
        }
    }
}

    post {
        success {
            echo 'PASSED: Selenium tests completed successfully.'
        }
        failure {
            // Updated message to be language-accurate
            echo 'FAILED: Python Selenium tests failed.'
        }
    }
