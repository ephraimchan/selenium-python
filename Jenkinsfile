pipeline {
    agent any

    // Removed the 'tools' block unless you have a specific 
    // Python installation defined in Global Tool Configuration.

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                // Ensure python3 is used if that's your environment
                sh 'python3 Basic_test-1.py' 
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
}