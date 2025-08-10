#!/usr/bin/env python3
"""
Startup script for the Arabic to Urdu Translation Agent
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'requests',
        'python-dotenv',
        'googletrans',
        'arabic-reshaper',
        'python-bidi',
        'langdetect'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    else:
        print("✅ All dependencies are installed!")
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        try:
            with open('.env.example', 'r') as example_file:
                example_content = example_file.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(example_content)
            
            print("✅ .env file created from template!")
        except FileNotFoundError:
            print("⚠️  .env.example not found, creating basic .env file...")
            with open('.env', 'w') as env_file:
                env_file.write("PORT=5000\nDEBUG=False\nSECRET_KEY=your-secret-key-here\n")
    else:
        print("✅ .env file already exists!")

def run_tests():
    """Run basic tests to ensure everything works"""
    print("🧪 Running basic tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_translation.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out!")
        return False
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Arabic to Urdu Translation Agent...")
    print("=" * 50)
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    
    try:
        # Import and run the app
        from app import app
        
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        print(f"📡 Server starting on port {port}")
        print(f"🔧 Debug mode: {debug}")
        print(f"🌐 Web interface: http://localhost:{port}")
        print(f"🔗 API endpoint: http://localhost:{port}/api/translate")
        print(f"🏥 Health check: http://localhost:{port}/health")
        print("\n" + "=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {str(e)}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🌟 Arabic to Urdu Translation Agent Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but continuing...")
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()