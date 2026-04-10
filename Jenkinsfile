pipeline {
    agent {
        docker {
            image 'my-selenium-python:latest'
        }
    }

    environment {
        // Selenium is in another container on same Docker network
        SELENIUM_HUB_URL = 'http://selenium-hub:4444'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
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
}