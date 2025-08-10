# Tenderly AI Agent - Docker Deployment Guide

This guide provides comprehensive instructions for dockerizing and deploying the Tenderly AI Agent using Docker and Docker Compose.

## 🏗️ Architecture Overview

The Tenderly AI Agent is a **FastAPI-based gynecology diagnosis service** that provides:

- **AI-Powered Diagnosis**: Uses OpenAI GPT-3.5 for medical diagnoses
- **Authentication**: JWT and API key-based authentication
- **Rate Limiting**: Redis-based rate limiting and caching
- **Health Monitoring**: Built-in health checks and monitoring endpoints
- **Production Ready**: Multi-stage Docker builds with security best practices

### Services Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │ Tenderly AI     │    │     Redis       │
│ (Reverse Proxy) │◄───┤    Agent        │◄───┤   (Cache)       │
│                 │    │  (FastAPI)      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └─────────────►│   Monitoring    │◄─────────────┘
                        │ (Prometheus +   │
                        │   Grafana)      │
                        └─────────────────┘
```

## 📋 Prerequisites

### System Requirements

- **Docker**: 20.10+ 
- **Docker Compose**: 2.0+
- **OpenSSL**: For generating secrets (usually pre-installed)
- **curl**: For health checks (usually pre-installed)

### Required Environment Variables

```bash
# Essential configuration
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=32_char_minimum_secret_key
JWT_SECRET_KEY=32_char_minimum_jwt_secret
API_KEY=32_char_minimum_api_key
```

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone and navigate to the repository
cd tenderly-ai-agent

# Run the setup script
./docker-deploy.sh setup
```

This script will:
- Check Docker requirements
- Create `.env` file from template
- Generate secure secrets
- Provide configuration guidance

### 2. Update Configuration

Edit the `.env` file with your actual values:

```bash
# Copy the generated secrets to .env
vim .env

# Required updates:
# - OPENAI_API_KEY: Your OpenAI API key
# - SECRET_KEY, JWT_SECRET_KEY, API_KEY: Generated secrets
# - CORS_ORIGINS: Your frontend domains
```

### 3. Build and Deploy

```bash
# Build Docker images
./docker-deploy.sh build

# Start services
./docker-deploy.sh start

# Check status
./docker-deploy.sh status

# Perform health check
./docker-deploy.sh health
```

### 4. Verify Deployment

```bash
# Check API health
curl http://localhost:8000/api/v1/health/live

# View API documentation (development mode)
open http://localhost:8000/docs
```

## 📁 Docker Files Overview

### Core Files

- **`Dockerfile`**: Multi-stage production build
- **`docker-compose.yml`**: Development deployment
- **`docker-compose.prod.yml`**: Production deployment with monitoring
- **`.dockerignore`**: Excludes unnecessary files from build context

### Configuration Files

- **`nginx/nginx.conf`**: Reverse proxy configuration
- **`redis/redis.conf`**: Redis configuration
- **`monitoring/prometheus.yml`**: Metrics collection
- **`.env.docker`**: Environment template

### Management Scripts

- **`docker-deploy.sh`**: Deployment automation script

## 🔧 Deployment Options

### Development Deployment

**Features:**
- Single service instance
- Debug mode enabled
- Direct port access
- Hot reload (if configured)

```bash
# Start development stack
./docker-deploy.sh start

# View logs
./docker-deploy.sh logs
```

**Services:**
- Tenderly AI Agent: `http://localhost:8000`
- Redis: `localhost:6379`

### Production Deployment

**Features:**
- Multiple service replicas
- Nginx reverse proxy with SSL
- Resource limits and monitoring
- Redis persistence
- Grafana dashboards

```bash
# Start production stack
./docker-deploy.sh start prod

# View production logs
./docker-deploy.sh logs prod
```

**Services:**
- Application: `https://localhost` (via Nginx)
- Monitoring: `http://localhost:3000` (Grafana)
- Metrics: `http://localhost:9090` (Prometheus)

## 🛠️ Management Commands

### Using docker-deploy.sh Script

```bash
# Setup and configuration
./docker-deploy.sh setup          # Initial setup
./docker-deploy.sh secrets        # Generate new secrets

# Build and deployment
./docker-deploy.sh build [prod]   # Build images
./docker-deploy.sh start [prod]   # Start services
./docker-deploy.sh stop [prod]    # Stop services
./docker-deploy.sh restart [prod] # Restart services

# Monitoring and debugging
./docker-deploy.sh status [prod]  # Show service status
./docker-deploy.sh logs [prod] [service] # View logs
./docker-deploy.sh health         # Health check

# Maintenance
./docker-deploy.sh cleanup [prod] # Clean up resources
```

### Direct Docker Compose

```bash
# Development
docker-compose up -d
docker-compose logs -f tenderly-ai-agent
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml down
```

## 🔐 Security Configuration

### Environment Variables

**Critical security settings:**

```bash
# Production secrets (generate with openssl rand -hex 32)
SECRET_KEY=your_32_character_secret_key_here
JWT_SECRET_KEY=your_32_character_jwt_secret_here
API_KEY=your_32_character_api_key_here

# API access control
ALLOWED_SERVICES=tenderly-backend,tenderly-frontend
CORS_ORIGINS=https://tenderly.care,https://app.tenderly.care

# Redis security
REDIS_PASSWORD=your_secure_redis_password
```

### SSL Certificate Setup

For production HTTPS, place your SSL certificates in:

```bash
nginx/ssl/server.crt  # SSL certificate
nginx/ssl/server.key  # SSL private key
```

Or use Let's Encrypt with cert-bot integration.

### Firewall Configuration

```bash
# Allow only necessary ports
# HTTP/HTTPS: 80, 443
# Application: 8000 (if direct access needed)
# Monitoring: 3000, 9090 (restrict to admin IPs)
```

## 📊 Monitoring and Logging

### Health Check Endpoints

```bash
# Liveness probe
curl http://localhost:8000/api/v1/health/live

# Readiness probe
curl http://localhost:8000/api/v1/health/ready

# Full health check
curl http://localhost:8000/api/v1/health/
```

### Log Management

```bash
# Application logs
./docker-deploy.sh logs tenderly-ai-agent

# Nginx logs
./docker-deploy.sh logs nginx

# Redis logs
./docker-deploy.sh logs redis

# Follow logs in real-time
docker-compose logs -f --tail=100 tenderly-ai-agent
```

### Monitoring Stack (Production)

- **Prometheus**: Metrics collection (`http://localhost:9090`)
- **Grafana**: Dashboards (`http://localhost:3000`)
- **Redis Exporter**: Redis metrics
- **Application Metrics**: Custom FastAPI metrics

## 🔧 Troubleshooting

### Common Issues

**1. Container Won't Start**
```bash
# Check logs for specific error
./docker-deploy.sh logs [service]

# Check configuration
docker-compose config

# Rebuild images
./docker-deploy.sh build --no-cache
```

**2. Health Check Fails**
```bash
# Check if service is running
./docker-deploy.sh status

# Check network connectivity
docker exec -it tenderly-ai-agent_tenderly-ai-agent_1 curl localhost:8000/api/v1/health/live

# Check environment variables
docker exec -it tenderly-ai-agent_tenderly-ai-agent_1 env | grep -E "(OPENAI|REDIS)"
```

**3. Redis Connection Issues**
```bash
# Check Redis container
docker exec -it tenderly-ai-agent_redis_1 redis-cli ping

# Check network
docker network ls
docker network inspect tenderly-ai-agent_tenderly-network
```

**4. OpenAI API Errors**
```bash
# Validate API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models

# Check application logs
./docker-deploy.sh logs | grep -i openai
```

### Performance Tuning

**Resource Limits:**
```yaml
# In docker-compose.prod.yml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

**Redis Configuration:**
```bash
# Adjust memory limits in redis/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

## 🚀 Production Deployment Checklist

- [ ] **Environment Configuration**
  - [ ] Update `.env` with production values
  - [ ] Generate secure secrets (32+ characters)
  - [ ] Configure CORS origins
  - [ ] Set proper API keys

- [ ] **Security Setup**
  - [ ] SSL certificates configured
  - [ ] Redis password set
  - [ ] API access controls defined
  - [ ] Network security configured

- [ ] **Infrastructure**
  - [ ] Docker and Docker Compose installed
  - [ ] Sufficient system resources allocated
  - [ ] Backup strategy implemented
  - [ ] Monitoring configured

- [ ] **Testing**
  - [ ] Health checks passing
  - [ ] API endpoints functional
  - [ ] Authentication working
  - [ ] Rate limiting effective

## 📝 API Usage

### Authentication

```bash
# Get JWT token (implement your auth endpoint)
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}' | jq -r '.token')

# Use API with token
curl -X POST http://localhost:8000/api/v1/diagnosis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["vaginal discharge", "itching"],
    "patient_age": 25,
    "severity_level": "moderate",
    "duration": "3 days"
  }'
```

### Example Response

```json
{
  "diagnosis": "Vaginal Candidiasis (Yeast Infection)",
  "confidence_score": 0.85,
  "suggested_investigations": [
    {
      "name": "Vaginal pH test",
      "priority": "medium",
      "reason": "To confirm diagnosis"
    }
  ],
  "recommended_medications": [
    {
      "name": "Fluconazole",
      "dosage": "150mg",
      "frequency": "Once",
      "duration": "Single dose"
    }
  ],
  "disclaimer": "This is an AI-generated diagnosis and should not replace professional medical consultation."
}
```

## 🆘 Support

For issues and questions:

1. **Check Logs**: Use `./docker-deploy.sh logs` to diagnose issues
2. **Health Checks**: Verify all services with `./docker-deploy.sh health`
3. **Configuration**: Review `.env` file and Docker Compose configuration
4. **Documentation**: Refer to the main README.md for application-specific details

## ⚖️ License

This project is licensed under the MIT License.

## ⚠️ Medical Disclaimer

This AI diagnosis service is intended for educational and research purposes only. It should not replace professional medical consultation, diagnosis, or treatment. Always consult with qualified healthcare providers for medical advice.
