from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from translation_agent import ArabicToUrduTranslator
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize the translator
translator = ArabicToUrduTranslator()

@app.route('/')
def index():
    """Main page with translation interface"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """API endpoint for translation"""
    try:
        data = request.get_json()
        arabic_text = data.get('text', '').strip()
        
        if not arabic_text:
            return jsonify({
                'success': False,
                'error': 'No text provided for translation'
            }), 400
        
        # Perform translation
        result = translator.translate(arabic_text)
        
        return jsonify({
            'success': True,
            'original': arabic_text,
            'translated': result['translated_text'],
            'confidence': result.get('confidence', 0.0),
            'detected_language': result.get('detected_language', 'ar'),
            'processing_time': result.get('processing_time', 0)
        })
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Translation failed. Please try again.'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Arabic to Urdu Translation Agent',
        'version': '1.0.0'
    })

@app.route('/api/translate', methods=['POST'])
def api_translate():
    """REST API endpoint for programmatic access"""
    try:
        data = request.get_json()
        arabic_text = data.get('text', '').strip()
        
        if not arabic_text:
            return jsonify({
                'error': 'No text provided for translation'
            }), 400
        
        result = translator.translate(arabic_text)
        
        return jsonify({
            'original_text': arabic_text,
            'translated_text': result['translated_text'],
            'confidence': result.get('confidence', 0.0),
            'detected_language': result.get('detected_language', 'ar'),
            'processing_time_ms': result.get('processing_time', 0) * 1000
        })
        
    except Exception as e:
        logger.error(f"API translation error: {str(e)}")
        return jsonify({
            'error': 'Translation service unavailable'
        }), 503

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting Arabic to Urdu Translation Agent...")
    print(f"📡 Server will run on port {port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)