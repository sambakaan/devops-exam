pipeline {
    agent any

    environment {
        CI_PROJECT = 'bibliotheque-ci'
        CI_NETWORK = 'bibliotheque-ci_bibliotheque-net'
        POSTGRES_USER     = 'bibliotheque'
        POSTGRES_PASSWORD = 'changeme'
        POSTGRES_DB       = 'bibliotheque'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'docker compose -f docker-compose.test.yml -p ${CI_PROJECT} up -d postgres'

                sh '''
                    status="starting"
                    for i in $(seq 1 30); do
                        status=$(docker inspect -f '{{.State.Health.Status}}' ${CI_PROJECT}-postgres-1 2>/dev/null || echo starting)
                        [ "$status" = "healthy" ] && break
                        sleep 2
                    done
                    [ "$status" = "healthy" ] || { echo "CI postgres never became healthy"; exit 1; }
                '''
                script {
                    docker.image('python:3.12-slim').inside("--network ${CI_NETWORK} -u root") {
                        withEnv([
                            "DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}",
                            'JWT_SECRET_KEY=test-secret-key',
                            'JWT_ALGORITHM=HS256',
                            'JWT_EXPIRATION_MINUTES=1440',
                            'LIVRES_SERVICE_URL=http://livres-service:8002',
                            'UTILISATEURS_SERVICE_URL=http://utilisateurs-service:8001'
                        ]) {
                            dir('utilisateurs-service') {
                                sh 'pip install --no-cache-dir -q -r requirements.txt && pytest -v'
                            }
                            dir('livres-service') {
                                sh 'pip install --no-cache-dir -q -r requirements.txt && pytest -v'
                            }
                            dir('emprunts-service') {
                                sh 'pip install --no-cache-dir -q -r requirements.txt && pytest -v'
                            }
                        }
                    }
                }
            }
            post {
                always {
                    sh 'docker compose -f docker-compose.test.yml -p ${CI_PROJECT} down -v || true'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose -p bibliotheque build'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: 'bibliotheque-env', variable: 'ENV_FILE')]) {
                    sh 'cp "$ENV_FILE" .env'
                }
                sh 'docker compose -p bibliotheque up -d --build'
            }
        }
    }
}
