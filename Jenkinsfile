pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                bat 'pip install selenium pytest'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'pytest Basic_test-1.py -v'
            }
        }
    }
    post {
        always {
            junit 'results.xml'
        }
    }
}