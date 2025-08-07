#!/usr/bin/env python3
"""
Script to check and fix your .env file for the AI News Anchor app
Run this to diagnose and fix API key issues
"""

import os
import sys

def check_env_file():
    """Check and fix the .env file"""
    
    print("=" * 60)
    print("AI NEWS ANCHOR - Environment File Checker")
    print("=" * 60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        create_new = input("\nWould you like to create one? (y/n): ").lower()
        if create_new == 'y':
            create_env_file()
        return
    
    # Read and analyze .env file
    print("\n📄 Reading .env file...")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        print(f"Found {len(lines)} lines in .env file\n")
        
        # Show current content (hiding most of the token)
        print("Current .env content:")
        print("-" * 40)
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if 'TOKEN' in key.upper() or 'KEY' in key.upper():
                        # Hide most of the token for security
                        if len(value) > 10:
                            print(f"Line {i}: {key}={value[:10]}...{value[-5:]}")
                        else:
                            print(f"Line {i}: {key}=<short_value>")
                    else:
                        print(f"Line {i}: {line}")
                else:
                    print(f"Line {i}: {line} ⚠️ (Invalid format - missing '=')")
            elif line.startswith('#'):
                print(f"Line {i}: {line[:50]}... (comment)")
            else:
                print(f"Line {i}: (empty line)")
        print("-" * 40)
        
        # Check for common issues
        print("\n🔍 Checking for common issues...\n")
        
        issues_found = False
        bearer_token = None
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if 'BEARER_TOKEN' in line:
                if '=' in line:
                    key, value = line.split('=', 1)
                    bearer_token = value.strip()
                    
                    # Check for quotes
                    if value.startswith('"') or value.startswith("'"):
                        print(f"⚠️  Line {i}: Remove quotes around the token value")
                        issues_found = True
                    
                    # Check if it includes "Bearer " prefix
                    if value.lower().startswith('bearer '):
                        print(f"⚠️  Line {i}: Remove 'Bearer ' prefix from the token")
                        print("   The token should start with something like 'eyJ...'")
                        issues_found = True
                    
                    # Check token format (should be JWT-like)
                    if not value.startswith('eyJ') and not value.startswith('"eyJ') and not value.startswith("'eyJ"):
                        print(f"⚠️  Line {i}: Token doesn't look like a JWT token")
                        print("   D-ID tokens typically start with 'eyJ'")
                        issues_found = True
        
        if not bearer_token:
            print("❌ No BEARER_TOKEN found in .env file!")
            issues_found = True
        
        if not issues_found:
            print("✅ No obvious issues found with .env file")
            print("\nIf you're still getting 401 errors, the token might be:")
            print("  1. Expired - Generate a new one at d-id.com")
            print("  2. Invalid - Double-check you copied it correctly")
            print("  3. Lacking permissions - Check API settings")
        else:
            print("\n❌ Issues found! Please fix the problems above.")
            fix_now = input("\nWould you like to re-enter your API token? (y/n): ").lower()
            if fix_now == 'y':
                create_env_file()
                
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        print("\nTry deleting the .env file and running this script again.")

def create_env_file():
    """Create a new .env file with proper formatting"""
    
    print("\n📝 Creating new .env file...")
    print("\nPlease enter your D-ID API Bearer Token.")
    print("ℹ️  Instructions:")
    print("  1. Go to https://studio.d-id.com/account-settings")
    print("  2. Navigate to 'API Keys' section")
    print("  3. Create or copy your API key")
    print("  4. Paste ONLY the token (not including 'Bearer ')")
    print("  5. The token should start with 'eyJ'")
    print()
    
    token = input("Enter your D-ID Bearer Token: ").strip()
    
    # Remove common mistakes
    if token.lower().startswith('bearer '):
        token = token[7:]  # Remove "Bearer " prefix
        print("✅ Removed 'Bearer ' prefix")
    
    # Remove quotes if present
    token = token.strip('"').strip("'")
    
    # Validate token format
    if not token.startswith('eyJ'):
        print("\n⚠️  Warning: Token doesn't start with 'eyJ' - this might not be correct!")
        proceed = input("Continue anyway? (y/n): ").lower()
        if proceed != 'y':
            return
    
    # Write to file
    try:
        with open('.env', 'w') as f:
            f.write(f"# D-ID API Configuration\n")
            f.write(f"BEARER_TOKEN={token}\n")
        
        print("\n✅ .env file created successfully!")
        print(f"   Token starts with: {token[:10]}...")
        print(f"   Token ends with: ...{token[-5:]}")
        print(f"   Token length: {len(token)} characters")
        
        # Test the token
        test = input("\nWould you like to test the API connection? (y/n): ").lower()
        if test == 'y':
            test_api_connection(token)
            
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def test_api_connection(token):
    """Test the D-ID API connection"""
    
    print("\n🧪 Testing API connection...")
    
    try:
        import requests
        
        url = "https://api.d-id.com/credits"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            credits = response.json()
            print(f"Credits remaining: {credits.get('remaining', 'N/A')}")
            print(f"Credits used: {credits.get('used', 'N/A')}")
        elif response.status_code == 401:
            print("❌ Authentication failed!")
            print("The token is invalid or expired. Please get a new one from d-id.com")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text}")
            
    except ImportError:
        print("⚠️  'requests' library not installed. Install it with: pip install requests")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    check_env_file()
    print("\n" + "=" * 60)
    print("Check complete! Now try running: streamlit run app.py")
    print("=" * 60)