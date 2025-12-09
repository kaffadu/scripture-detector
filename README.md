Scripture Detection and Projection System
📖 Overview
An end-to-end application that continuously listens to church preaching, detects Bible scripture references in real-time, and projects them to a screen. Supports multiple Bible versions with NKJV as default.

🎯 Features
Real-time Audio Processing: Listens to speaker and processes audio continuously

Scripture Detection: Identifies Bible references in spoken text

Multi-version Support: Default NKJV with ability to change versions

Real-time Projection: WebSocket-based screen projection

Version Preference Storage: Redis-based version persistence

Kubernetes Ready: Full container orchestration support

CI/CD Pipeline: Jenkins with SonarQube integration

ArgoCD Deployment: GitOps for Kubernetes deployments

🏗️ Architecture
text
Audio Input → Speech Recognition → Scripture Detection → Bible API → Screen Projection
     ↑              ↑                    ↑                   ↑            ↑
 Microphone     Google Speech       Pattern Matching     API.Bible    WebSocket
                                            ↓
                                      Redis (Version Storage)
📁 Project Structure
text
scripture-detector/
├── app/                          # Main application
│   ├── src/                      # Source code
│   │   ├── main.py              # Application entry point
│   │   ├── audio_processor.py   # Audio capture and processing
│   │   ├── scripture_detector.py # Scripture reference detection
│   │   ├── bible_api.py         # Bible API integration
│   │   ├── screen_projector.py  # WebSocket projection server
│   │   └── config.py            # Configuration management
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile               # Container definition
├── kubernetes/                   # K8s manifests
│   ├── deployment.yaml          # Deployment configuration
│   ├── service.yaml             # Service definitions
│   ├── configmap.yaml           # Configuration
│   └── ingress.yaml             # Ingress routing
├── projection-ui/               # Web projection interface
├── Jenkinsfile                  # CI/CD pipeline
├── docker-compose.yaml          # Local development
├── sonar-project.properties     # SonarQube configuration
└── README.md                    # This file
🚀 Quick Start
Prerequisites
Python 3.9+

Docker & Docker Compose

Bible API Key (from API.Bible)

Microphone (for audio input)

Installation Steps
1. Clone and Setup
bash
# Clone the repository
git clone <repository-url>
cd scripture-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt
2. Configure Environment
bash
# Copy environment template
cp app/.env.example app/.env

# Edit .env file with your API key
# Add your Bible API key and other configurations
3. Local Development
bash
# Run with Docker Compose
docker-compose up -d

# Or run locally
cd app
python -m src.main
4. Access the Application
WebSocket Server: ws://localhost:8765

Projection UI: http://localhost:8080

Redis: localhost:6379

🔧 Configuration
Environment Variables
Variable	Description	Default
BIBLE_API_KEY	API.Bible access key	Required
GOOGLE_SPEECH_API_KEY	Google Speech-to-Text API key	Optional
REDIS_HOST	Redis server hostname	localhost
REDIS_PORT	Redis server port	6379
REDIS_DB	Redis database number	0
AUDIO_SAMPLE_RATE	Audio sampling rate	16000
DEFAULT_BIBLE_VERSION	Default Bible version	NKJV
WEBSOCKET_PORT	WebSocket server port	8765
Bible API Setup
Visit API.Bible

Sign up for a free account

Generate an API key

Add the key to your .env file

🐳 Docker Deployment
Build Image
bash
docker build -t scripture-detector:latest -f app/Dockerfile .
Run Container
bash
docker run -d \
  -p 8765:8765 \
  -p 6379:6379 \
  -e BIBLE_API_KEY="your_key_here" \
  --device /dev/snd:/dev/snd \
  scripture-detector:latest
☸️ Kubernetes Deployment
Prerequisites
Kubernetes Cluster (v1.19+)

kubectl configured

ArgoCD installed (optional)

Deployment Steps
1. Create Namespace
bash
kubectl create namespace scripture
2. Create ConfigMap
bash
# Update configmap.yaml with your API key
kubectl apply -f kubernetes/configmap.yaml -n scripture
3. Create Secrets (if needed)
bash
kubectl create secret generic bible-api-key \
  --from-literal=BIBLE_API_KEY="your_key_here" \
  -n scripture
4. Deploy Application
bash
kubectl apply -f kubernetes/deployment.yaml -n scripture
kubectl apply -f kubernetes/service.yaml -n scripture
kubectl apply -f kubernetes/ingress.yaml -n scripture
5. Verify Deployment
bash
kubectl get all -n scripture
kubectl get pods -n scripture
kubectl logs -f deployment/scripture-detector -n scripture
🔄 CI/CD Pipeline (Jenkins)
Pipeline Setup
1. Jenkins Requirements
Jenkins with Docker pipeline plugin

SonarQube server configured

Docker Registry access

Kubernetes credentials

2. Jenkins Credentials
Create the following credentials in Jenkins:

Docker Registry Credentials

ID: docker-credentials

Username/Password for your registry

SonarQube Token

ID: sonar-token

Token from SonarQube server

Kubernetes kubeconfig (optional)

For direct Kubernetes deployment

3. Pipeline Configuration
bash
# Update Jenkinsfile with your configuration:
# - DOCKER_REGISTRY: Your container registry URL
# - SONAR_HOST_URL: Your SonarQube server URL
# - Deployment namespace and settings
4. Create Jenkins Pipeline
In Jenkins, create a new "Pipeline" job

Set "Pipeline script from SCM"

Select Git and provide repository URL

Set branch to main

Script path: Jenkinsfile

5. Pipeline Stages
The pipeline includes:

Code Checkout

Dependency Installation

SonarQube Analysis

Unit Testing

Docker Build

Security Scan (Trivy)

Registry Push

Kubernetes Deployment

📊 SonarQube Integration
Setup SonarQube
Install SonarQube (if not already installed)

Create Project in SonarQube

Generate Token for the project

Configuration
Update sonar-project.properties:

properties
sonar.projectKey=scripture-detector
sonar.host.url=http://your-sonarqube:9000
sonar.login=your_token_here
Run SonarQube Analysis Locally
bash
# Install sonar-scanner
# Run analysis
sonar-scanner \
  -Dsonar.projectKey=scripture-detector \
  -Dsonar.sources=app/src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your_token
🚢 ArgoCD Deployment (GitOps)
Prerequisites
ArgoCD installed in your cluster

Git repository with manifests

ArgoCD Application Setup
Create argocd/application.yaml:

yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: scripture-detector
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/your-org/scripture-detector.git'
    targetRevision: HEAD
    path: kubernetes
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: scripture
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
Deploy with ArgoCD
bash
# Apply ArgoCD application
kubectl apply -f argocd/application.yaml -n argocd

# Monitor sync status
argocd app get scripture-detector
🎮 Usage
Starting the Application
bash
# Local development
python -m src.main

# With Docker
docker-compose up

# With Kubernetes
kubectl apply -f kubernetes/
Changing Bible Version
1. Via Speech
The speaker can say:

"Let's read from the NIV version"

"Switch to ESV"

"Use King James Version"

2. Via Web Interface
Access the projection UI and use the version selector dropdown.

3. Programmatically
python
# Change version via API
import requests
response = requests.post(
    'http://localhost:8765/version',
    json={'version': 'NIV'}
)
Projection Screen
Open http://localhost:8080 in a browser

Connect to a projector or large screen

The screen will automatically update when scriptures are detected

🧪 Testing
Run Unit Tests
bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
cd app
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
Test Audio Processing
bash
# Test microphone
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"

# Test speech recognition
python -m src.audio_processor --test
🔍 Monitoring and Logging
Logs
bash
# View application logs
docker-compose logs -f scripture-app

# Kubernetes logs
kubectl logs -f deployment/scripture-detector -n scripture

# Redis logs
kubectl logs -f deployment/redis -n scripture
Metrics
The application exposes metrics on port 8765:

Connection count

Scripture detection rate

Version change count

Health Checks
bash
# WebSocket health check
curl -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     -H "Sec-WebSocket-Version: 13" \
     http://localhost:8765/

# API health check
curl http://localhost:8765/health
🛠️ Troubleshooting
Common Issues
1. Audio Not Detected
bash
# Check microphone permissions
ls -la /dev/snd/

# Test with arecord
arecord --duration=5 --format=dat test.wav

# On macOS, check sound preferences
2. Bible API Errors
bash
# Verify API key
echo $BIBLE_API_KEY

# Test API connection
curl -H "api-key: YOUR_KEY" \
  https://api.scripture.api.bible/v1/bibles
3. WebSocket Connection Issues
bash
# Check if port is open
netstat -tlnp | grep 8765

# Test WebSocket connection
wscat -c ws://localhost:8765
4. Redis Connection Problems
bash
# Test Redis connection
redis-cli -h localhost -p 6379 ping

# Check Redis logs
docker-compose logs redis
Debug Mode
Enable debug logging:

bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in Kubernetes
kubectl set env deployment/scripture-detector LOG_LEVEL=DEBUG -n scripture
📈 Scaling
Horizontal Pod Autoscaling
Create kubernetes/hpa.yaml:

yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: scripture-detector-hpa
  namespace: scripture
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: scripture-detector
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
Database Scaling
For production:

Use Redis Cluster instead of single instance

Add persistent volume claims

Configure backups

🔒 Security
Security Best Practices
API Key Management

Use Kubernetes Secrets

Rotate keys regularly

Limit API key permissions

Network Security

Use HTTPS for WebSocket

Implement authentication for projection UI

Use network policies

Container Security

Run as non-root user

Regular vulnerability scanning

Keep dependencies updated

Security Scanning
bash
# Scan for vulnerabilities
trivy image scripture-detector:latest

# Check for secrets in code
gitleaks --path . --verbose

# Dependency scanning
safety check -r app/requirements.txt
📚 API Documentation
WebSocket API
Endpoint: ws://host:8765

Messages Received
Scripture updates in JSON format

Version change notifications

Connection status

Example Message
json
{
  "reference": "John 3:16",
  "text": "For God so loved the world...",
  "version": "NKJV",
  "type": "scripture"
}
REST API (Optional)
Add REST endpoints for manual control:

python
# Example endpoints
POST /version    # Change Bible version
GET /status      # Get application status
POST /scripture  # Manually add scripture
🤝 Contributing
Development Workflow
Fork the repository

Create a feature branch

Make changes

Add tests

Run tests and linting

Submit pull request

Code Style
bash
# Install pre-commit hooks
pip install pre-commit black flake8 mypy
pre-commit install

# Run formatting
black app/src/

# Run linting
flake8 app/src/

# Type checking
mypy app/src/
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
API.Bible for Bible text API

Google Speech-to-Text for speech recognition

Redis for data storage

WebSockets for real-time communication

📞 Support
For issues and questions:

GitHub Issues: Create an issue in the repository

Email: support@yourdomain.com

Documentation: Check the Wiki

Note: This application requires a Bible API key from API.Bible. Free tier available with limited requests.

Version: 1.0.0
Last Updated: 2024
