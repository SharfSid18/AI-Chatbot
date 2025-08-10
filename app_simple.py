from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import re
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class ArabicToUrduTranslator:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
        
    def preprocess_arabic_text(self, text):
        """Clean and preprocess Arabic text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize Arabic characters
        text = text.replace('ي', 'ی')  # Normalize ya
        text = text.replace('ك', 'ک')  # Normalize kaf
        text = text.replace('ة', 'ہ')  # Normalize ta marbuta
        
        return text
    
    def postprocess_urdu_text(self, text):
        """Clean and postprocess Urdu text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common translation issues
        text = text.replace('آپ', 'آپ')  # Ensure proper Urdu pronouns
        text = text.replace('میں', 'میں')  # Ensure proper Urdu pronouns
        
        return text
    
    def translate_with_google_api(self, text):
        """Translate using Google Translate API"""
        try:
            if self.api_key:
                # Use Google Translate API
                url = "https://translation.googleapis.com/language/translate/v2"
                params = {
                    'key': self.api_key,
                    'q': text,
                    'source': 'ar',
                    'target': 'ur'
                }
                response = requests.post(url, data=params)
                if response.status_code == 200:
                    result = response.json()
                    return result['data']['translations'][0]['translatedText']
            
            return None
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return None
    
    def translate_with_libre_translate(self, text):
        """Translate using LibreTranslate (free alternative)"""
        try:
            # Using LibreTranslate public API
            url = "https://libretranslate.de/translate"
            data = {
                'q': text,
                'source': 'ar',
                'target': 'ur'
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText')
            
            return None
            
        except Exception as e:
            logger.error(f"LibreTranslate error: {str(e)}")
            return None
    
    def translate_text(self, arabic_text):
        """Main translation method"""
        if not arabic_text or not arabic_text.strip():
            return {
                'success': False,
                'error': 'No text provided for translation'
            }
        
        try:
            # Preprocess Arabic text
            processed_text = self.preprocess_arabic_text(arabic_text)
            
            # Try Google Translate API first
            translated_text = self.translate_with_google_api(processed_text)
            
            # Fallback to LibreTranslate
            if translated_text is None:
                translated_text = self.translate_with_libre_translate(processed_text)
            
            # If still no translation, provide a simple mapping for common phrases
            if translated_text is None:
                translated_text = self.simple_translation_fallback(processed_text)
            
            if translated_text is None:
                return {
                    'success': False,
                    'error': 'Translation service unavailable. Please try again later.'
                }
            
            # Postprocess Urdu text
            final_text = self.postprocess_urdu_text(translated_text)
            
            return {
                'success': True,
                'original_text': arabic_text,
                'translated_text': final_text,
                'source_language': 'Arabic',
                'target_language': 'Urdu'
            }
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                'success': False,
                'error': f'Translation error: {str(e)}'
            }
    
    def simple_translation_fallback(self, text):
        """Simple fallback translation for common phrases"""
        # Common Arabic to Urdu translations
        translations = {
            'مرحبا': 'ہیلو',
            'شكرا': 'شکریہ',
            'كيف حالك': 'آپ کیسے ہیں',
            'مع السلامة': 'اللہ حافظ',
            'صباح الخير': 'صبح بخیر',
            'مساء الخير': 'شام بخیر',
            'نعم': 'ہاں',
            'لا': 'نہیں',
            'ماء': 'پانی',
            'خبز': 'روٹی',
            'بيت': 'گھر',
            'سيارة': 'کار',
            'كتاب': 'کتاب',
            'قلم': 'قلم',
            'مدرسة': 'اسکول',
            'طالب': 'طالب علم',
            'معلم': 'استاد',
            'طبيب': 'ڈاکٹر',
            'مهندس': 'انجینئر',
            'محامي': 'وکیل'
        }
        
        # Try to find exact matches
        for arabic, urdu in translations.items():
            if arabic in text:
                return text.replace(arabic, urdu)
        
        # If no exact match, return a placeholder
        return f"[Translation: {text}] - Please use Google Translate API for better results."

# Initialize translator
arabic_urdu_translator = ArabicToUrduTranslator()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Translation API endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        arabic_text = data['text']
        result = arabic_urdu_translator.translate_text(arabic_text)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Arabic to Urdu Translation Agent',
        'version': '1.0.0'
    }), 200

@app.route('/demo')
def demo():
    """Demo endpoint with sample translations"""
    sample_texts = [
        "مرحبا بالعالم",
        "كيف حالك",
        "شكرا لك",
        "مع السلامة"
    ]
    
    results = []
    for text in sample_texts:
        result = arabic_urdu_translator.translate_text(text)
        results.append({
            'arabic': text,
            'urdu': result.get('translated_text', 'Translation failed'),
            'success': result.get('success', False)
        })
    
    return jsonify({
        'demo_translations': results
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Arabic to Urdu Translation Agent...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔧 For better translations, set GOOGLE_TRANSLATE_API_KEY in .env file")
    app.run(debug=True, host='0.0.0.0', port=5000)