# Tenderly AI Agent - Authentication Guide

## 🔐 Authentication Methods

The Tenderly AI Agent supports **two authentication methods**:

1. **API Key Authentication** (Recommended for service-to-service)
2. **JWT Bearer Token Authentication** (Recommended for user sessions)

## 🚀 Quick Setup Summary

After dockerizing the application, I've fixed the authentication issues and generated secure credentials:

### Generated Secure Credentials:
- **API_KEY**: `9e5883f3f2596b3c3d0be7e399b0f147a06b3c9b34ed29f775bd091f8bb3d350`
- **JWT_SECRET_KEY**: `146ab4fec2f968c24c218f404054f7e4a69d3526c8811a9c431ce1d555863f65`
- **SECRET_KEY**: `4fe02dddc90413bab2a40b037c4e5c26c5feb34caea01629316f533bdd6e3ea5`

## 📋 Method 1: API Key Authentication

### Configuration
```bash
# Headers required:
X-API-Key: 9e5883f3f2596b3c3d0be7e399b0f147a06b3c9b34ed29f775bd091f8bb3d350
X-Service-Name: tenderly-backend  # Optional but recommended
Content-Type: application/json
```

### Example Request
```bash
curl -X POST 'http://localhost:8000/api/v1/diagnosis/' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: 9e5883f3f2596b3c3d0be7e399b0f147a06b3c9b34ed29f775bd091f8bb3d350' \
  -H 'X-Service-Name: tenderly-backend' \
  -d '{
    "diagnosis_request": {
        "symptoms": ["Missed Period", "Pelvic Pain"],
        "patient_age": 25,
        "severity_level": "severe",
        "duration": "3 days",
        "onset": "sudden",
        "progression": "worsening"
    }
}'
```

### Allowed Services
- `tenderly-backend`
- `tenderly-frontend`  
- `tenderly-admin`

## 🎫 Method 2: JWT Bearer Token Authentication

### Token Generation
Use the provided `generate_token.py` script:

```bash
python3 generate_token.py
```

**Sample Generated Token:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMTIzIiwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTQ4MDM2ODIsImlhdCI6MTc1NDgwMDA4Mn0.BjGUEiCYD9kD2mU8_l5y5-QNve6CbnwbL1La82k9Rmw
```

### Example Request
```bash
curl -X POST http://localhost:8000/api/v1/diagnosis/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMTIzIiwidXNlcm5hbWUiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTQ4MDM2ODIsImlhdCI6MTc1NDgwMDA4Mn0.BjGUEiCYD9kD2mU8_l5y5-QNve6CbnwbL1La82k9Rmw" \
  -d '{
    "diagnosis_request": {
      "symptoms": ["vaginal discharge", "itching"],
      "patient_age": 25,
      "severity_level": "moderate", 
      "duration": "3 days"
    }
  }'
```

## ✅ Successful Response Example

```json
{
  "diagnosis": "Possible Ectopic Pregnancy",
  "confidence_score": 0.7,
  "suggested_investigations": [
    {
      "name": "Transvaginal Ultrasound",
      "priority": "high",
      "reason": "To visualize the uterus and fallopian tubes for signs of ectopic pregnancy"
    }
  ],
  "recommended_medications": [
    {
      "name": "Methotrexate",
      "dosage": "As prescribed by a healthcare provider",
      "frequency": "As prescribed",
      "duration": "As prescribed",
      "notes": "This medication is used to treat ectopic pregnancies, but its use should be closely monitored by a healthcare provider"
    }
  ],
  "lifestyle_advice": [
    "Avoid strenuous physical activity",
    "Seek immediate medical attention if experiencing severe pelvic pain or vaginal bleeding"
  ],
  "follow_up_recommendations": "Immediate follow-up with a healthcare provider for further evaluation and management",
  "disclaimer": "This diagnosis is AI-generated and should not replace professional medical consultation. Always consult with a qualified healthcare provider for medical advice.",
  "timestamp": "2025-08-10T04:26:35.180656"
}
```

## 🔧 What Was Fixed

### Issue Identified:
- **Missing Environment Variables**: API key authentication variables were not being passed to Docker containers
- **Incorrect API Key**: The API key in the request didn't match the configured one
- **Docker Compose Configuration**: Missing API key environment variables in docker-compose.yml

### Solutions Applied:

#### 1. Updated Docker Compose Configuration
Added missing environment variables to `docker-compose.yml`:
```yaml
# API Key Authentication
- API_KEY=${API_KEY}
- ALLOWED_SERVICES=${ALLOWED_SERVICES:-tenderly-backend,tenderly-frontend,tenderly-admin}
- API_KEY_HEADER_NAME=${API_KEY_HEADER_NAME:-X-API-Key}
- REQUIRE_SERVICE_NAME=${REQUIRE_SERVICE_NAME:-true}
- ALLOWED_IPS=${ALLOWED_IPS:-127.0.0.1,::1}
```

#### 2. Generated Secure Secrets
Used the deployment script to generate production-grade secrets:
```bash
./docker-deploy.sh secrets
```

#### 3. Updated Environment File
Updated `.env` with secure 64-character hex keys:
- **API_KEY**: `9e5883f3f2596b3c3d0be7e399b0f147a06b3c9b34ed29f775bd091f8bb3d350`
- **JWT_SECRET_KEY**: `146ab4fec2f968c24c218f404054f7e4a69d3526c8811a9c431ce1d555863f65`
- **SECRET_KEY**: `4fe02dddc90413bab2a40b037c4e5c26c5feb34caea01629316f533bdd6e3ea5`

#### 4. Restarted Services
```bash
./docker-deploy.sh restart
```

## 🛠️ Troubleshooting

### Common Authentication Errors

#### 1. "Invalid API key"
**Solution**: Use the correct API key from environment:
```bash
X-API-Key: 9e5883f3f2596b3c3d0be7e399b0f147a06b3c9b34ed29f775bd091f8bb3d350
```

#### 2. "Missing API key"
**Solution**: Ensure the header name is correct:
```bash
X-API-Key: [your-api-key]  # Not "Authorization" or "Api-Key"
```

#### 3. JWT Token Expired
**Solution**: Generate a new token:
```bash
python3 generate_token.py
```

#### 4. Service Not Allowed
**Solution**: Use an allowed service name:
```bash
X-Service-Name: tenderly-backend  # or tenderly-frontend, tenderly-admin
```

### Verification Commands

```bash
# Check if services are running
./docker-deploy.sh status

# Check health endpoints
./docker-deploy.sh health

# Check environment variables in container
docker exec tenderly-ai-agent-tenderly-ai-agent-1 printenv | grep API_KEY

# View application logs
docker logs tenderly-ai-agent-tenderly-ai-agent-1 --tail 20
```

## 🔒 Security Best Practices

### For Production Deployment:

1. **Rotate Secrets Regularly**
   ```bash
   ./docker-deploy.sh secrets  # Generate new keys
   # Update .env file
   ./docker-deploy.sh restart  # Apply changes
   ```

2. **Use Environment-Specific Keys**
   - Development: Current generated keys
   - Staging: Different set of keys
   - Production: Highly secure, regularly rotated keys

3. **Network Security**
   - Use HTTPS in production (SSL certificates in nginx)
   - Restrict `ALLOWED_IPS` to specific networks
   - Configure proper CORS origins

4. **Monitoring**
   - Monitor failed authentication attempts
   - Set up alerts for unusual API usage patterns
   - Log all API key usage for audit trails

## 📞 Support

If you encounter authentication issues:

1. **Check Container Environment**:
   ```bash
   docker exec tenderly-ai-agent-tenderly-ai-agent-1 printenv | grep -E "(API_KEY|JWT_SECRET_KEY)"
   ```

2. **Verify Request Format**:
   - Correct headers: `X-API-Key` and `X-Service-Name`
   - Proper JSON format in request body
   - Valid service name from allowed list

3. **Check Application Logs**:
   ```bash
   docker logs tenderly-ai-agent-tenderly-ai-agent-1 | grep -i auth
   ```

---

**Status**: ✅ **Authentication Working Successfully**

Both API Key and JWT authentication methods are now fully functional with the dockerized Tenderly AI Agent!
