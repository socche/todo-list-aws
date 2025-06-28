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
    }
}