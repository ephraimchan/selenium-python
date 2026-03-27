pipeline {
    agent any

    tools {
        maven 'Python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh 'python Basic_test-1.py'
            }
        }
    }

    post {
            always {
               
            }

            success {
                // This only runs if all tests pass
                echo 'PASSED: Selenium tests completed successfully on the Grid.'
            }

            failure {
                // This only runs if at least one test fails
                echo 'FAILED: Selenium tests failed. Check TestNG Results for details.'
                // You can also add archiveArtifacts here to save logs
            }

    }
}