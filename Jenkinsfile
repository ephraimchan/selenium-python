pipeline {
    agent {
        docker { 
            
            image 'my-selenium-python:latest'
            // This allows the container to talk back to your Docker host if needed
            args '-v /var/run/docker.sock:/var/run/docker.sock'
            }
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
        always {
        // This looks for the XML report created by pytest
        junit '**/nosetests.xml' 
    }

   
}
} // End of pipeline