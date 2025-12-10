pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'index.docker.io'
        IMAGE_NAME = 'scripture-detector'
        SONAR_HOST_URL = 'http://192.168.1.164/:9000'
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
            steps {
                sh '''
                   sudo apt-get update
                    sudo apt-get install -y python3 python3-venv python3-pip
                    python3 --version
                    python3 -m venv "${VENV_PATH}"
                    
                    if [ -f "${VENV_PATH}/bin/activate" ]; then
                        echo "Virtual environment created"
                    else
                        echo "Failed to create virtual environment"
                        exit 1
                    fi
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    source "${VENV_PATH}/bin/activate"
                    which python
                    which pip
                    pip install --upgrade pip
                    pip install app/requirements.txt
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
            steps {
                sh '''
                    cd app
                    python -m pytest tests/ -v --cov=src --cov-report=xml
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
