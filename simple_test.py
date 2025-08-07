#!/usr/bin/env python3
"""
Ultra-simple D-ID API test using their exact documentation format
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Your API key from .env
api_key = os.getenv("BEARER_TOKEN", "")

if not api_key:
    print("No API key found in .env file!")
    exit(1)

print(f"Using API key: {api_key[:20]}...{api_key[-10:]}\n")

# Use D-ID's own example from their documentation
url = "https://api.d-id.com/talks"

# Simplest possible payload - exactly as per D-ID docs
payload = {
    "source_url": "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg",
    "script": {
        "type": "text",
        "input": "Hello, this is a test"
    }
}

# Since your key has a colon, it's likely Basic auth with base64 encoding
import base64

# Try different auth methods
auth_methods = []

# Method 1: Basic with base64 encoding (standard Basic auth)
encoded = base64.b64encode(api_key.encode()).decode('ascii')
auth_methods.append(("Basic (base64)", f"Basic {encoded}"))

# Method 2: Bearer with full key
auth_methods.append(("Bearer (full)", f"Bearer {api_key}"))

# Method 3: Basic with raw key
auth_methods.append(("Basic (raw)", f"Basic {api_key}"))

# Method 4: If it's email:token, try just the token
if ':' in api_key:
    token_only = api_key.split(':')[1]
    auth_methods.append(("Bearer (token only)", f"Bearer {token_only}"))

print("Testing D-ID API with different authentication methods...\n")
print("=" * 60)

for method_name, auth_header in auth_methods:
    print(f"\nTrying: {method_name}")
    print("-" * 40)
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": auth_header
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201 or response.status_code == 200:
            print("✅ SUCCESS!")
            result = response.json()
            print(f"Talk ID: {result.get('id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            print("\n🎉 FOUND WORKING METHOD!")
            print(f"Use this authorization: {method_name}")
            print("=" * 60)
            
            # Save the working method
            with open("working_auth.txt", "w") as f:
                f.write(f"Working method: {method_name}\n")
                f.write(f"Authorization header: {auth_header}\n")
            
            break
            
        elif response.status_code == 401:
            print("❌ Unauthorized - Wrong credentials")
            
        elif response.status_code == 402:
            print("❌ Payment Required - Check your D-ID credits")
            
        elif response.status_code == 500:
            print("⚠️  Server Error (500) - D-ID server issue")
            print("Error details:", response.text[:300])
            
        else:
            print(f"❌ Error: {response.status_code}")
            print("Response:", response.text[:300])
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

print("\n" + "=" * 60)
print("\nIf all methods failed with 500 errors, it's likely a D-ID server issue.")
print("Try again in a few minutes or contact D-ID support.")
print("\nIf you got 401 errors, your API key format might be incorrect.")
print("Check https://studio.d-id.com/api-keys to verify your key.")