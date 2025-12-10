pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'index.docker.io'
        IMAGE_NAME = 'scripture-detector'
        SONAR_HOST_URL = 'http://192.168.1.164:9000'
        SONAR_TOKEN = credentials('sonarqube')
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                sh '''
                    # Use the Python image that includes venv/ensurepip
                    if command -v python3 >/dev/null 2>&1; then
                        PY=python3
                    elif command -v python >/dev/null 2>&1; then
                        PY=python
                    else
                        echo "Python is not available in the container."
                        exit 1
                    fi

                    $PY --version
                    $PY -m venv "${VENV_PATH}"

                    if [ -f "${VENV_PATH}/bin/activate" ]; then
                        echo "Virtual environment created at ${VENV_PATH}"
                    else
                        echo "Failed to create virtual environment"
                        exit 1
                    fi
                '''
            }
        }

        stage('Install Dependencies') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                sh '''
                    source "${VENV_PATH}/bin/activate"
                    which python
                    which pip
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                    pip list
                '''
            }
        }

        stage('Code Quality - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=scripture-detector \
                          -Dsonar.sources=app/src \
                          -Dsonar.host.url=${SONAR_HOST_URL} \
                          -Dsonar.login=${SONAR_TOKEN} \
                          -Dsonar.python.version=3.9
                    '''
                }
            }
        }

        stage('Unit Tests') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                sh '''
                    source "${VENV_PATH}/bin/activate"
                    "${VENV_PATH}/bin/python" -m pytest app/tests/ -v --cov=app/src --cov-report=xml
                '''
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                    cobertura coberturaReportFile: '**/coverage.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    trivy image --format table \
                      --exit-code 0 \
                      --severity HIGH,CRITICAL \
                      ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-cred') {
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        kubectl set image deployment/scripture-detector \
                          main=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                          --namespace=default

                        kubectl rollout status deployment/scripture-detector \
                          --namespace=default
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            emailext(
                subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Check console output at ${env.BUILD_URL}",
                to: 'team@yourdomain.com'
            )
        }
    }
}
