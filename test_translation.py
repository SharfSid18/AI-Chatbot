#!/usr/bin/env python3
"""
Test script for Arabic to Urdu Translation Agent
"""

import requests
import json
import time

def test_translation():
    """Test the translation functionality"""
    
    # Test cases
    test_cases = [
        {
            "arabic": "مرحبا بالعالم",
            "expected_urdu": "ہیلو ورلڈ"
        },
        {
            "arabic": "كيف حالك",
            "expected_urdu": "آپ کیسے ہیں"
        },
        {
            "arabic": "شكرا لك",
            "expected_urdu": "آپ کا شکریہ"
        }
    ]
    
    print("🧪 Testing Arabic to Urdu Translation Agent")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the application is running.")
        print("   Run: python app.py")
        return
    
    # Test translations
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{test_case['arabic']}'")
        
        try:
            response = requests.post(
                "http://localhost:5000/translate",
                json={"text": test_case["arabic"]},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result["success"]:
                    urdu_text = result["translated_text"]
                    print(f"✅ Translation successful")
                    print(f"   Arabic: {test_case['arabic']}")
                    print(f"   Urdu: {urdu_text}")
                else:
                    print(f"❌ Translation failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("\n🔍 Testing API Endpoints")
    print("=" * 30)
    
    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/", "Main page"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:5000{endpoint}")
            else:
                response = requests.post(f"http://localhost:5000{endpoint}")
            
            if response.status_code in [200, 302]:  # 302 for redirects
                print(f"✅ {description}: {response.status_code}")
            else:
                print(f"❌ {description}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {e}")

if __name__ == "__main__":
    print("🚀 Starting Arabic to Urdu Translation Agent Tests")
    print("Make sure the application is running on http://localhost:5000")
    print()
    
    test_api_endpoints()
    test_translation()