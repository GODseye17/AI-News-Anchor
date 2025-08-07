#!/usr/bin/env python3
"""
Quick test script to verify D-ID API connection
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("BEARER_TOKEN")

if not api_key:
    print("❌ No BEARER_TOKEN found in .env file!")
    exit(1)

print("=" * 60)
print("D-ID API Connection Test")
print("=" * 60)
print(f"\n✅ API Key loaded: {api_key[:20]}...{api_key[-10:]}")
print(f"   Key length: {len(api_key)} characters\n")

# Test different authentication methods
print("Testing authentication methods...\n")

# Method 1: As Bearer token
print("1. Testing as Bearer token...")
headers1 = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

try:
    response = requests.get("https://api.d-id.com/credits", headers=headers1)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Success with Bearer format!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Method 2: As Basic auth (if it's email:password format)
print("2. Testing as Basic auth...")
headers2 = {
    "accept": "application/json",
    "authorization": f"Basic {api_key}"
}

try:
    response = requests.get("https://api.d-id.com/credits", headers=headers2)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Success with Basic format!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Method 3: Test the talks endpoint directly
print("3. Testing talks endpoint with minimal payload...")
url = "https://api.d-id.com/talks"
payload = {
    "script": {
        "type": "text",
        "input": "Hello world",
        "provider": {
            "type": "microsoft",
            "voice_id": "en-US-JennyNeural"
        }
    },
    "source_url": "https://i.ibb.co/hYcxXTW/anchor.png"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Basic {api_key}"  # Try Basic first
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"   Basic auth - Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print("   ✅ Success with Basic auth!")
        print(f"   Response: {response.json()}")
    else:
        # Try with Bearer
        headers["authorization"] = f"Bearer {api_key}"
        response = requests.post(url, json=payload, headers=headers)
        print(f"   Bearer auth - Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   ✅ Success with Bearer auth!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Both methods failed")
            print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)