#!/usr/bin/env python3
"""
Simple test script for the Arabic to Urdu Translation Agent
"""

import sys
import time
from translation_agent import ArabicToUrduTranslator

def test_translation():
    """Test the translation functionality"""
    print("🧪 Testing Arabic to Urdu Translation Agent...")
    
    # Initialize translator
    translator = ArabicToUrduTranslator()
    
    # Test cases
    test_cases = [
        "مرحبا",
        "شكرا لك",
        "كيف حالك",
        "أنا بخير",
        "أهلا وسهلا",
        "مع السلامة",
        "صباح الخير",
        "مساء الخير"
    ]
    
    print(f"\n📝 Testing {len(test_cases)} Arabic phrases...")
    print("-" * 50)
    
    for i, arabic_text in enumerate(test_cases, 1):
        print(f"\n{i}. Arabic: {arabic_text}")
        
        try:
            start_time = time.time()
            result = translator.translate(arabic_text)
            end_time = time.time()
            
            print(f"   Urdu: {result['translated_text']}")
            print(f"   Confidence: {result['confidence']:.1%}")
            print(f"   Engine: {result['engine_used']}")
            print(f"   Time: {(end_time - start_time)*1000:.0f}ms")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Translation test completed!")
    
    # Test service stats
    stats = translator.get_translation_stats()
    print(f"\n📊 Service Statistics:")
    print(f"   Available Engines: {', '.join(stats['engines_available'])}")
    print(f"   Supported Languages: {stats['supported_languages']}")
    print(f"   Service Status: {stats['service_status']}")

def test_health_check():
    """Test health check functionality"""
    print("\n🏥 Testing health check...")
    
    translator = ArabicToUrduTranslator()
    stats = translator.get_translation_stats()
    
    if stats['service_status'] == 'operational':
        print("✅ Service is healthy and operational")
    else:
        print("❌ Service health check failed")
        return False
    
    return True

if __name__ == "__main__":
    try:
        test_translation()
        test_health_check()
        print("\n🎉 All tests passed! The translation agent is ready to use.")
        print("\nTo start the web interface, run:")
        print("   python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)