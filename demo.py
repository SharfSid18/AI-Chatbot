#!/usr/bin/env python3
"""
Demo script for Arabic to Urdu Translation Agent
Shows the application in action with sample translations
"""

import requests
import json
import time

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🌍 Arabic to Urdu Translation Agent - Demo")
    print("=" * 60)
    print()

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service: {data['service']}")
            print(f"✅ Status: {data['status']}")
            print(f"✅ Version: {data['version']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the application is running.")
        print("   Run: python3 app.py")
        return False
    print()
    return True

def test_translations():
    """Test various translations"""
    print("🔄 Testing Translations...")
    print()
    
    # Sample Arabic texts with expected meanings
    test_cases = [
        ("مرحبا", "Hello"),
        ("شكرا لك", "Thank you"),
        ("كيف حالك", "How are you"),
        ("مع السلامة", "Goodbye"),
        ("صباح الخير", "Good morning"),
        ("مساء الخير", "Good evening"),
        ("نعم", "Yes"),
        ("لا", "No"),
        ("ماء", "Water"),
        ("خبز", "Bread"),
        ("بيت", "House"),
        ("سيارة", "Car"),
        ("كتاب", "Book"),
        ("قلم", "Pen"),
        ("مدرسة", "School")
    ]
    
    for i, (arabic, english_meaning) in enumerate(test_cases, 1):
        print(f"📝 Test {i:2d}: {arabic} ({english_meaning})")
        
        try:
            response = requests.post(
                "http://localhost:5000/translate",
                json={"text": arabic},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result["success"]:
                    urdu_text = result["translated_text"]
                    print(f"   ✅ Urdu: {urdu_text}")
                else:
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")
        
        print()

def test_demo_endpoint():
    """Test the demo endpoint"""
    print("🎯 Testing Demo Endpoint...")
    try:
        response = requests.get("http://localhost:5000/demo")
        if response.status_code == 200:
            data = response.json()
            translations = data.get('demo_translations', [])
            
            print(f"✅ Found {len(translations)} demo translations:")
            for i, trans in enumerate(translations, 1):
                print(f"   {i}. {trans['arabic']} → {trans['urdu']}")
        else:
            print(f"❌ Demo endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Demo endpoint error: {e}")
    print()

def show_web_interface_info():
    """Show information about the web interface"""
    print("🌐 Web Interface Information")
    print("=" * 40)
    print("📱 URL: http://localhost:5000")
    print("🎨 Features:")
    print("   • Beautiful, responsive design")
    print("   • Real-time character counting")
    print("   • Copy and download functionality")
    print("   • Keyboard shortcuts (Ctrl+Enter)")
    print("   • Mobile-friendly interface")
    print("   • Toast notifications")
    print()

def show_api_info():
    """Show API information"""
    print("🔌 API Endpoints")
    print("=" * 30)
    print("GET  /health     - Health check")
    print("GET  /           - Web interface")
    print("GET  /demo       - Demo translations")
    print("POST /translate  - Translate text")
    print()
    print("📝 Translation API Usage:")
    print("curl -X POST http://localhost:5000/translate \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"text\": \"مرحبا\"}'")
    print()

def main():
    """Main demo function"""
    print_banner()
    
    # Test if server is running
    if not test_health():
        return
    
    # Show API information
    show_api_info()
    
    # Test translations
    test_translations()
    
    # Test demo endpoint
    test_demo_endpoint()
    
    # Show web interface info
    show_web_interface_info()
    
    print("🎉 Demo completed successfully!")
    print("💡 For the best experience, open http://localhost:5000 in your browser")
    print("🔧 To improve translation quality, add your Google Translate API key to .env file")

if __name__ == "__main__":
    main()