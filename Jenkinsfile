pipeline {
    agent {
        docker { 
            image 'my-selenium-python:latest'
            // Keep this if you want the container to have Docker-in-Docker capability
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        // Essential for Docker Desktop on Windows
        SELENIUM_HUB_URL = 'http://host.docker.internal:4444' 
        DOCKER_HOST = 'tcp://localhost:2375'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                // Ensure the filename matches your actual .py file
                sh 'python3 -m pytest -v Basic_test-1.py --junitxml=results.xml || true'
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
        always {
            junit testResults: 'results.xml', allowEmptyResults: true
        }
    }
} // End of pipeline