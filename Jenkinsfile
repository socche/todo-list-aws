pipeline {
    agent none

    environment {
        PATH = "/home/agente1/.local/bin:$PATH"
    }

    stages {
        stage('Get Code') {
            agent { label 'agente1' }
            steps {
                sh 'whoami'
                sh 'hostname'
                git branch: 'master', url: 'https://github.com/socche/todo-list-aws.git'
                sh 'git clone --single-branch --branch production https://github.com/socche/todo-list-aws-config.git config'
                sh 'cp config/samconfig.toml .'
            }
        }

        stage('Deploy (Production)') {
            agent { label 'agente1' }
            steps {
                sh 'whoami'
                sh 'hostname'
                echo 'Building project with SAM...'
                sh 'sam build'

                echo 'Validating template...'
                sh 'sam validate --region us-east-1'

                echo 'Deploying to Production environment...'
                sh 'sam deploy --config-env production --no-confirm-changeset || true'

                stash name: 'workspace-cd', includes: '**/*'
            }
        }

        stage('REST Test') {
            agent { label 'agente2' }
            environment {
                BASE_URL = 'https://iw3lwsx0mj.execute-api.us-east-1.amazonaws.com/Prod'
                PATH = "/home/agente2/.local/bin:$PATH"
            }
            steps {
                unstash 'workspace-cd'
                sh 'whoami'
                sh 'hostname'

                echo 'Ejecutando tests de lectura en entorno de producción...'
                sh 'pytest --junitxml=report.xml test/integration/test_readonly.py'

                echo 'Publicando resultados...'
                junit 'report.xml'
            }
        }

        stage('Limpieza') {
            agent { label 'agente2' }
            steps {
                sh 'whoami'
                sh 'hostname'
                echo 'Limpiando entorno de trabajo...'
                cleanWs()
            }
        }
    }
}