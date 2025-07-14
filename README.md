# Tenderly AI Agent - Gynecology Diagnosis Service

A production-grade AI diagnosis microservice for gynecology care using FastAPI and OpenAI GPT-3.5.

## Features

- **AI-Powered Diagnosis**: Uses OpenAI GPT-3.5 for generating medical diagnoses
- **Production Ready**: Includes authentication, rate limiting, logging, and monitoring
- **Secure**: JWT authentication, input validation, and secure API practices
- **Scalable**: Redis-based rate limiting and caching
- **Monitored**: Health checks and structured logging
- **Containerized**: Docker support for easy deployment

## Architecture

### Core Components

- **FastAPI**: Modern, fast web framework for APIs
- **OpenAI GPT-3.5**: AI model for diagnosis generation
- **Redis**: Rate limiting and caching
- **Pydantic**: Data validation and serialization
- **JWT**: Authentication and authorization
- **Structured Logging**: Comprehensive logging for monitoring

### Project Structure

```
tenderly-ai-agent/
├── app/
│   ├── config/          # Configuration settings
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   ├── routers/         # API endpoints
│   ├── middleware/      # Auth and rate limiting
│   ├── utils/           # Utilities and logging
│   ├── exceptions/      # Custom exceptions
│   └── main.py          # FastAPI app
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Development setup
└── README.md           # This file
```

## Quick Start

### Prerequisites

- **Python 3.8+** (Recommended: 3.11+)
- **Redis** (for rate limiting and caching)
- **OpenAI API Key** (for AI diagnosis generation)
- **Git** (for cloning the repository)

### Installation

#### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/tenderly-ai-agent.git
cd tenderly-ai-agent
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.1

# Security Configuration
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Application Configuration
APP_NAME=Tenderly AI Agent
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=development

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_SSL=false

# API Configuration
API_PREFIX=/api/v1
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://tenderly.care
```

#### 5. Set Up Redis

**Option A: Install Redis locally**

```bash
# On macOS (using Homebrew):
brew install redis
brew services start redis

# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# On Windows:
# Download Redis from https://redis.io/download
# Or use Windows Subsystem for Linux (WSL)
```

#### 6. Generate Security Keys

Generate secure JWT secret keys:

```bash
# Run the token generator
python generate_token.py
```

Copy the generated keys to your `.env` file.

#### 7. Run the Application

**Development Mode:**

```bash
# Run with hot reload
python run.py


#### 8. Verify Installation

Check if the application is running:

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health/

# Access interactive API documentation
# Open http://localhost:8000/docs in your browser
```

## API Endpoints

### Health Check
- `GET /api/v1/health/` - Full health check
- `GET /api/v1/health/live` - Liveness probe
- `GET /api/v1/health/ready` - Readiness probe

### Diagnosis
- `POST /api/v1/diagnosis/` - Generate AI diagnosis
- `POST /api/v1/diagnosis/validate` - Validate symptoms

### Authentication

All diagnosis endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Usage Example

### Generate Diagnosis

```bash
curl -X POST "http://localhost:8000/api/v1/diagnosis/" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["vaginal discharge", "itching", "burning sensation"],
    "patient_age": 25,
    "medical_history": ["diabetes"],
    "severity_level": "moderate",
    "duration": "3 days",
    "additional_notes": "Symptoms worsen at night"
  }'
```

### Response Format

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
      "duration": "Single dose",
      "notes": "Oral antifungal medication"
    }
  ],
  "lifestyle_advice": [
    "Wear breathable cotton underwear",
    "Avoid tight-fitting clothes",
    "Maintain good hygiene"
  ],
  "follow_up_recommendations": "Follow up in 1 week if symptoms persist",
  "disclaimer": "This is an AI-generated diagnosis and should not replace professional medical consultation.",
  "timestamp": "2023-11-15T10:30:00Z"
}
```

## Configuration

### Environment Variables

Key configuration options (see `.env.example` for full list):

- `OPENAI_API_KEY` - OpenAI API key
- `JWT_SECRET_KEY` - JWT signing secret
- `REDIS_HOST` - Redis server host
- `RATE_LIMIT_REQUESTS` - Rate limit per window
- `DEBUG` - Enable debug mode

### Security Features

- **JWT Authentication**: Token-based authentication
- **Rate Limiting**: Configurable rate limits per user/IP
- **Input Validation**: Comprehensive input sanitization
- **HTTPS**: Force secure connections in production
- **CORS**: Configurable cross-origin resource sharing

## Integration

### With NestJS Backend

```typescript
// Example NestJS service
@Injectable()
export class DiagnosisService {
  constructor(private readonly httpService: HttpService) {}

  async getDiagnosis(symptoms: string[], patientInfo: any, token: string) {
    const response = await this.httpService.post(
      'http://tenderly-ai-agent:8000/api/v1/diagnosis/',
      {
        symptoms,
        patient_age: patientInfo.age,
        medical_history: patientInfo.medicalHistory,
        severity_level: patientInfo.severity,
        duration: patientInfo.duration,
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    
    return response.data;
  }
}
```

## Testing

Run tests:
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_diagnosis.py

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run tests with coverage and generate HTML report
pytest --cov=app --cov-report=html --cov-report=term
```

## Troubleshooting

### Common Issues

#### 1. Redis Connection Error
```bash
redis.exceptions.ConnectionError: Error connecting to Redis
```
**Solution:** Make sure Redis is running:
```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
brew services start redis  # macOS
sudo systemctl start redis-server  # Linux
```

#### 2. OpenAI API Key Error
```bash
OpenAIServiceError: OpenAI API call failed
```
**Solution:** Check your OpenAI API key:
- Ensure `OPENAI_API_KEY` is set in your `.env` file
- Verify the API key is valid and has sufficient credits
- Check OpenAI service status at https://status.openai.com/

#### 3. JWT Token Error
```bash
HTTP 401: Unauthorized
```
**Solution:** Generate or verify JWT tokens:
```bash
# Generate new JWT secret
python generate_token.py

# Update .env file with new JWT_SECRET_KEY
```

#### 4. Port Already in Use
```bash
OSError: [Errno 48] Address already in use
```
**Solution:** Use a different port or kill the process:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --port 8001
```

#### 5. Module Not Found Error
```bash
ModuleNotFoundError: No module named 'app'
```
**Solution:** Make sure you're running from the correct directory:
```bash
# Check current directory
pwd

# Should be in the project root
cd /path/to/tenderly-ai-agent

# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG

# Or export as environment variable
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Logs

Check application logs:

```bash
# View logs in real-time
tail -f logs/app.log

# Search for errors
grep -i error logs/app.log

# View structured logs
cat logs/app.log | jq .
```

## Deployment

### Production Deployment

1. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_key_here
   export JWT_SECRET_KEY=your_secret_here
   export ENVIRONMENT=production
   export DEBUG=False
   ```

2. **Deploy with Docker**:
   ```bash
   docker build -t tenderly-ai-agent .
   docker run -p 8000:8000 --env-file .env tenderly-ai-agent
   ```

### Kubernetes Deployment

The service includes health check endpoints for Kubernetes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tenderly-ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tenderly-ai-agent
  template:
    metadata:
      labels:
        app: tenderly-ai-agent
    spec:
      containers:
      - name: tenderly-ai-agent
        image: tenderly-ai-agent:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /api/v1/health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /api/v1/health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

## Monitoring

### Logging

The service uses structured logging with:
- Request/response logging
- Error tracking
- Performance metrics
- Audit trails

### Health Monitoring

- **Liveness**: Service is running
- **Readiness**: Service can handle requests
- **Health**: Comprehensive status including external dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Medical Disclaimer

This AI diagnosis service is intended for educational and research purposes only. It should not replace professional medical consultation, diagnosis, or treatment. Always consult with qualified healthcare providers for medical advice.

## Support

For support or questions, please contact the development team.
