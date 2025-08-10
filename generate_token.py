#!/usr/bin/env python
"""Generate JWT token for testing the AI Diagnosis Agent."""

from datetime import datetime, timedelta, timezone
from jose import jwt

# Your secret key from the .env file
secret_key = '146ab4fec2f968c24c218f404054f7e4a69d3526c8811a9c431ce1d555863f65'
algorithm = 'HS256'

# Create the payload
payload = {
    'sub': 'test_user_123',
    'username': 'test_user',
    'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # Expires in 1 hour
    'iat': datetime.now(timezone.utc),  # Issued at
}

# Encode the token
token = jwt.encode(payload, secret_key, algorithm=algorithm)
print(f"JWT Token: {token}")
print("\nUse this token in your API requests:")
print(f"Authorization: Bearer {token}")
print("\nExample curl command:")
print(f"""curl -X POST http://localhost:8000/api/v1/diagnosis/ \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer {token}" \\
  -d '{{
    "diagnosis_request": {{
      "symptoms": ["vaginal discharge", "itching"],
      "patient_age": 25,
      "severity_level": "moderate",
      "duration": "3 days"
    }}
  }}'""")