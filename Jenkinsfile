pipeline {
    agent {
        docker {
            image 'my-selenium-python:latest'
            // This is the critical line to link the containers
            args '--network automation-network'
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
                //sh 'python3 -m pytest --collect-only'
                sh 'python3 -m pytest -v test_basic_1.py --junitxml=results.xml || true'
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