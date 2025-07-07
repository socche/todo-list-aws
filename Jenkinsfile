pipeline {
    agent none

    stages {
        stage('Get Code') {
            agent { label 'agente1' }
            steps {
                git credentialsId: 'github-token-id',
                    branch: 'develop',
                    url: 'https://github.com/socche/todo-list-aws.git'

                dir('config') {
                    deleteDir()
                }

                sh 'git clone --single-branch --branch staging https://github.com/socche/todo-list-aws-config.git config'
                sh 'cp config/samconfig.toml .'
            }
        }

        stage('Static Test') {
            agent { label 'agente1' }
            steps {
                echo 'Running flake8...'
                sh 'flake8 src/ || true'
                echo 'Running bandit...'
                sh 'bandit -r src/ || true'
            }
        }

        stage('Deploy (Staging)') {
            agent { label 'agente1' }
            steps {
                echo 'Building project with SAM...'
                sh 'sam build'

                echo 'Validating template...'
                sh 'sam validate --region us-east-1'

                echo 'Deploying to Staging environment (expecting failure)...'
                sh 'sam deploy --config-env staging --no-confirm-changeset || true'

                stash name: 'workspace-ci', includes: '**/*'
            }
        }

        stage('REST Test') {
            agent { label 'agente2' }
            environment {
                BASE_URL = 'https://iw3lwsx0mj.execute-api.us-east-1.amazonaws.com/Prod'
            }
            steps {
                unstash 'workspace-ci'
                echo 'Running REST integration tests...'
                sh '/usr/local/bin/pytest --junitxml=report.xml test/integration/todoApiTest.py'

                echo 'Publicando resultados...'
                junit 'report.xml'
            }
        }

        stage('Merge to master') {
            agent { label 'agente1' }
            when {
                branch 'develop'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-token-id', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
                    echo 'Haciendo merge a master...'
                    sh '''
                        git config user.name "Javier Collado"
                        git config user.email "socche@gmail.com"
                        git config --global merge.ours.driver true

                        git fetch --all

                        echo "Actualizando rama develop..."
                        git checkout develop
                        git pull origin develop

                        echo "Actualizando rama master..."
                        git checkout master
                        git pull origin master

                        echo "Haciendo merge local desde develop (no origin/develop)..."
                        git merge develop --no-edit || true

                        echo "Haciendo push a master..."
                        git push https://${GIT_USERNAME}:${GIT_TOKEN}@github.com/socche/todo-list-aws.git master
                    '''
                }
            }
        }
    }
}