pipeline {
    agent any

    tools {
        maven 'Maven3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh 'mvn clean test'
            }
        }
    }

    post {
            always {
                // This runs every time to update your charts
                step([$class: 'Publisher', reportFilenamePattern: '**/testng-results.xml'])
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