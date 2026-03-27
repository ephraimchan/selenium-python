pipeline {
    agent {
        docker { image 'python:3.9-slim' }
    }

    environment {
        // host.docker.internal works if Jenkins is on Docker Desktop (Windows/Mac)
        // If on Linux, you might need your actual LAN IP here.
        SELENIUM_HUB_URL = 'http://host.docker.internal:4444' 
    }

    stages {
        stage('Checkout') {
            steps {
                // This pulls your code from Git/SCM into the workspace
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'pip install selenium'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 Basic_test-1.py'
            }
        }
    }

    // The post block must be INSIDE the pipeline braces
    post {
        success {
            echo 'PASSED: Selenium tests completed successfully.'
        }
        failure {
            echo 'FAILED: Python Selenium tests failed.'
        }
    }
} // End of pipeline