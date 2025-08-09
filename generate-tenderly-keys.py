#!/usr/bin/env python3
"""
Tenderly Key Generator
Generates secure authentication keys for Tenderly services
"""

import secrets
import string
import json
import base64
from datetime import datetime
import sys
import os

class TenderlyKeyGenerator:
    """Generate secure keys for Tenderly service ecosystem"""
    
    @staticmethod
    def generate_secure_key(length_bytes=32):
        """Generate a cryptographically secure random key (base64 encoded)"""
        return base64.b64encode(secrets.token_bytes(length_bytes)).decode('utf-8')
    
    @staticmethod
    def generate_hex_key(length_bytes=32):
        """Generate a hex-encoded key"""
        return secrets.token_hex(length_bytes)
    
    @staticmethod
    def generate_api_key(length=64):
        """Generate an alphanumeric API key suitable for HTTP headers"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def generate_tenderly_keys():
        """Generate a complete set of keys for Tenderly services"""
        
        # Generate timestamp
        timestamp = datetime.now().isoformat()
        
        keys = {
            # Shared JWT secret (CRITICAL: must be same across all services)
            "JWT_SECRET_KEY": TenderlyKeyGenerator.generate_secure_key(32),
            
            # AI Agent API key for service-to-service authentication
            "AI_DIAGNOSIS_API_KEY": TenderlyKeyGenerator.generate_api_key(64),
            
            # Individual service application secrets
            "BACKEND_SECRET_KEY": TenderlyKeyGenerator.generate_secure_key(32),
            "AI_AGENT_SECRET_KEY": TenderlyKeyGenerator.generate_secure_key(32),
            
            # Additional security keys for future use
            "ENCRYPTION_KEY": TenderlyKeyGenerator.generate_secure_key(32),
            "SIGNING_KEY": TenderlyKeyGenerator.generate_secure_key(32),
            
            # Metadata
            "GENERATED_AT": timestamp,
            "KEY_VERSION": "v1.0.0",
            "GENERATOR": "Tenderly Key Generator",
            
            # Instructions
            "_README": {
                "JWT_SECRET_KEY": "Shared across ALL services for JWT validation",
                "AI_DIAGNOSIS_API_KEY": "Used by backend to authenticate with AI agent",
                "BACKEND_SECRET_KEY": "Backend service application secret",
                "AI_AGENT_SECRET_KEY": "AI agent service application secret",
                "NEXT_ROTATION": "Recommended in 90 days (quarterly JWT rotation)"
            }
        }
        
        return keys
    
    @staticmethod
    def save_keys(keys, filename="tenderly-keys.json"):
        """Save keys to JSON file"""
        with open(filename, 'w') as f:
            json.dump(keys, f, indent=2)
    
    @staticmethod
    def print_env_format(keys):
        """Print keys in environment file format"""
        print("\n" + "="*60)
        print("ENVIRONMENT FILE FORMAT")
        print("="*60)
        
        print(f"\n# Tenderly Backend (.env)")
        print(f"# Location: /Users/asharansari/tenderly.care/tenderly-backend/.env")
        print(f"JWT_SECRET={keys['JWT_SECRET_KEY']}")
        print(f"AI_DIAGNOSIS_SECRET_KEY={keys['JWT_SECRET_KEY']}")
        print(f"AI_DIAGNOSIS_API_KEY={keys['AI_DIAGNOSIS_API_KEY']}")
        print(f"SECRET_KEY={keys['BACKEND_SECRET_KEY']}")
        print(f"AI_DIAGNOSIS_TOKEN_EXPIRY=3600")
        
        print(f"\n# Tenderly AI Agent (.env)")
        print(f"# Location: /Users/asharansari/tenderly.care/tenderly-ai-agent/.env")
        print(f"JWT_SECRET_KEY={keys['JWT_SECRET_KEY']}")
        print(f"API_KEY={keys['AI_DIAGNOSIS_API_KEY']}")
        print(f"SECRET_KEY={keys['AI_AGENT_SECRET_KEY']}")
        print(f"JWT_ALGORITHM=HS256")
        print(f"JWT_EXPIRATION_HOURS=24")
    
    @staticmethod
    def print_deployment_checklist():
        """Print deployment checklist"""
        print("\n" + "="*60)
        print("DEPLOYMENT CHECKLIST")
        print("="*60)
        print("""
□ 1. Backup current .env files
   cp /Users/asharansari/tenderly.care/tenderly-backend/.env \\
      /Users/asharansari/tenderly.care/tenderly-backend/.env.backup.$(date +%Y%m%d)
   cp /Users/asharansari/tenderly.care/tenderly-ai-agent/.env \\
      /Users/asharansari/tenderly.care/tenderly-ai-agent/.env.backup.$(date +%Y%m%d)

□ 2. Update backend .env file with new keys

□ 3. Update AI agent .env file with new keys

□ 4. Restart backend service:
   cd /Users/asharansari/tenderly.care/tenderly-backend
   pm2 restart tenderly-backend

□ 5. Restart AI agent service:
   cd /Users/asharansari/tenderly.care/tenderly-ai-agent
   pkill -f "uvicorn app.main:app"
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

□ 6. Test API key authentication:
   curl -X POST http://localhost:8000/api/v1/diagnosis/structure \\
     -H "X-API-Key: <NEW_API_KEY>" \\
     -H "X-Service-Name: tenderly-backend" \\
     -H "Content-Type: application/json" \\
     -d '{"structured_request": {"patient_profile": {"age": 28, "request_id": "test", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"}}}'

□ 7. Verify service health:
   curl http://localhost:3000/health
   curl http://localhost:8000/api/v1/health/live

□ 8. Monitor logs for authentication errors

□ 9. Document rotation completion

□ 10. Securely delete this file: rm tenderly-keys.json
        """)

def main():
    """Main function"""
    print("🔑 Tenderly Key Generator")
    print("=" * 50)
    
    try:
        # Generate keys
        print("Generating secure authentication keys...")
        keys = TenderlyKeyGenerator.generate_tenderly_keys()
        
        # Save to file
        filename = "tenderly-keys.json"
        TenderlyKeyGenerator.save_keys(keys, filename)
        
        print(f"✅ Keys generated successfully!")
        print(f"📄 Saved to: {filename}")
        
        # Display keys
        print(f"\n🔍 Generated Keys:")
        for key, value in keys.items():
            if not key.startswith('_') and key not in ['GENERATED_AT', 'KEY_VERSION', 'GENERATOR']:
                print(f"   {key}: {value}")
        
        # Print environment format
        TenderlyKeyGenerator.print_env_format(keys)
        
        # Print deployment checklist
        TenderlyKeyGenerator.print_deployment_checklist()
        
        print(f"\n⚠️  SECURITY NOTES:")
        print(f"   • Keep these keys secure and confidential")
        print(f"   • Update ALL services before the old keys expire")
        print(f"   • JWT_SECRET_KEY MUST be identical in all services")
        print(f"   • Delete {filename} after deployment")
        print(f"   • Next rotation recommended: {datetime.now().replace(month=datetime.now().month+3).strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"❌ Error generating keys: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
