pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                git branch: 'develop', url: 'https://github.com/socche/todo-list-aws.git'
            }
        }
        
        stage('Static Test') {
            steps {
                echo 'Running flake8...'
                sh 'flake8 src/ || true'
                
                echo 'Running bandit...'
                sh 'bandit -r src/ || true'
            }
        }
        
        stage('Deploy (Staging)') {
            steps {
                echo 'Building project with SAM...'
                sh 'sam build'

                echo 'Validating template...'
                sh 'sam validate --region us-east-1'

                echo 'Deploying to Staging environment (expecting failure)...'
                sh 'sam deploy --config-env staging --no-confirm-changeset'
            }
        }
        
        stage('REST Test') {
            environment {
                BASE_URL = 'https://iw3lwsx0mj.execute-api.us-east-1.amazonaws.com/Prod'
            }
            steps {
                echo 'Running REST integration tests...'
                sh 'pytest test/integration/todoApiTest.py'
            }
        }
    }
}