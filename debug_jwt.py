#!/usr/bin/env python3
"""Debug JWT token generation and validation."""

import os
import sys
from datetime import datetime, timedelta
from jose import jwt, JWTError
import json

# Add the current directory to the path so we can import app modules
sys.path.append('/Users/asharansari/tenderly.care/tenderly-ai-agent')

# JWT configuration
JWT_SECRET_KEY = "shared-jwt-secret-key-for-ai-agent"
JWT_ALGORITHM = "HS256"

def create_test_token():
    """Create a test JWT token like the backend would."""
    now = int(datetime.now().timestamp())
    expires_in = 3600  # 1 hour
    
    payload = {
        "sub": "tenderly-backend-service",
        "username": "backend-service",
        "exp": now + expires_in,
        "iat": now,
        "aud": "ai-diagnosis-service",
        "iss": "tenderly-backend",
        "service": True,
    }
    
    print(f"Current timestamp: {now} ({datetime.fromtimestamp(now)})")
    print(f"Expiry timestamp: {now + expires_in} ({datetime.fromtimestamp(now + expires_in)})")
    print("Creating token with payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_test_token(token):
    """Verify a JWT token like the AI agent would."""
    try:
        print(f"Verifying token: {token[:50]}...")
        print()
        
        # Try with audience validation first (how the token should work)
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )
            print("✅ Token verification successful with audience validation!")
            print("Decoded payload:")
            print(json.dumps(payload, indent=2))
            return payload
        except JWTError as e:
            print(f"❌ Token verification failed with audience validation: {e}")
            
        # Try without audience validation (current AI agent behavior)
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
                options={"verify_aud": False}  # Disable audience verification
            )
            print("⚠️  Token verification successful WITHOUT audience validation!")
            print("Decoded payload:")
            print(json.dumps(payload, indent=2))
            return payload
        except JWTError as e2:
            print(f"❌ Token verification failed even without audience validation: {e2}")
            return None
        
    except Exception as e:
        print(f"Unexpected error during verification: {e}")
        return None

def test_with_different_secrets():
    """Test with different secret keys to identify potential mismatch."""
    secrets_to_test = [
        "shared-jwt-secret-key-for-ai-agent",
        "your_jwt_secret_key_here",
        "development_secret_key_change_in_production",
        "tenderly-backend-secret"
    ]
    
    # Create token with the expected secret
    token = create_test_token()
    print(f"Token created: {token}\n")
    
    print("Testing token verification with different secrets:")
    print("-" * 50)
    
    for secret in secrets_to_test:
        try:
            payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
            print(f"✅ SUCCESS with secret: '{secret}'")
            print(f"   Subject: {payload.get('sub')}")
            return secret
        except JWTError as e:
            print(f"❌ FAILED with secret: '{secret}' - {e}")
    
    return None

if __name__ == "__main__":
    print("=== JWT Token Debug Tool ===")
    print()
    
    # Test 1: Basic token creation and verification
    print("Test 1: Basic token creation and verification")
    print("=" * 45)
    token = create_test_token()
    payload = verify_test_token(token)
    print()
    
    # Test 2: Try different secrets
    print("Test 2: Testing with different secret keys")
    print("=" * 45)
    working_secret = test_with_different_secrets()
    print()
    
    if working_secret:
        print(f"✅ Working secret found: '{working_secret}'")
    else:
        print("❌ No working secret found")
    
    print("\n=== Debug Complete ===")
