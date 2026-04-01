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
                // 1. We use 'pytest' instead of 'python3' to run the specific file
                // 2. We add the --junitxml flag to generate the report file
                // 3. We add '|| true' so the pipeline doesn't stop immediately if a test fails,
                //    allowing the 'post' block to still grab the report.
                sh 'pytest Basic_test-1.py --junitxml=results.xml || true'
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
        junit 'results.xml' 
    }

   
}
} // End of pipeline