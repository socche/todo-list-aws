pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                git branch: 'master', url: 'https://github.com/socche/todo-list-aws.git'
            }
        }

        stage('Deploy (Production)') {
            steps {
                echo 'Building project with SAM...'
                sh 'sam build'

                echo 'Validating template...'
                sh 'sam validate --region us-east-1'

                echo 'Deploying to Production environment...'
                sh 'sam deploy --config-env production --no-confirm-changeset || true'
            }
        }

        stage('REST Test') {
            environment {
                BASE_URL = 'https://iw3lwsx0mj.execute-api.us-east-1.amazonaws.com/Prod'
            }
            steps {
                echo 'Ejecutando tests de lectura en entorno de producción...'
                sh 'pytest --junitxml=report.xml test/integration/test_readonly.py'

                echo 'Publicando resultados...'
                junit 'report.xml'
            }
        }

        stage('Limpieza') {
            steps {
                echo 'Limpiando entorno de trabajo...'
                cleanWs()
            }
        }
    }
}
