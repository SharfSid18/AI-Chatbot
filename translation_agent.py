import time
import logging
import arabic_reshaper
from bidi.algorithm import get_display
import requests
import json
from typing import Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

class ArabicToUrduTranslator:
    """
    Professional Arabic to Urdu Translation Agent
    
    This class provides multiple translation engines and Arabic text preprocessing
    for accurate translation from Arabic to Urdu.
    """
    
    def __init__(self):
        """Initialize the translation agent with multiple engines"""
        self.translation_engines = {
            'google': self._translate_google,
            'fallback': self._translate_fallback
        }
        
        # Arabic text preprocessing patterns
        self.arabic_patterns = {
            'diacritics': re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED]'),
            'tashkeel': re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u08D4-\u08FE]'),
            'arabic_numbers': re.compile(r'[\u0660-\u0669]'),
            'arabic_punctuation': re.compile(r'[\u0600-\u0603\u0606-\u060A\u060C\u060D\u0610-\u061A\u061E\u0640\u064B-\u065F\u066A-\u066D\u0670\u06D4\u06D5\u06D6-\u06ED\u06F0-\u06F9\u06FD\u06FE\u08D4-\u08FE\uFB50-\uFDFF\uFE70-\uFEFF]')
        }
        
        logger.info("Arabic to Urdu Translation Agent initialized")
    
    def translate(self, arabic_text: str) -> Dict[str, Any]:
        """
        Translate Arabic text to Urdu with preprocessing and multiple engines
        
        Args:
            arabic_text (str): Input Arabic text
            
        Returns:
            Dict containing translation results and metadata
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not arabic_text or not arabic_text.strip():
                raise ValueError("Empty or invalid input text")
            
            # Preprocess Arabic text
            processed_text = self._preprocess_arabic_text(arabic_text)
            
            # Detect language
            detected_lang = self._detect_language(processed_text)
            
            if detected_lang != 'ar':
                logger.warning(f"Detected language is {detected_lang}, expected Arabic")
            
            # Try translation with multiple engines
            translation_result = self._translate_with_fallback(processed_text)
            
            processing_time = time.time() - start_time
            
            return {
                'translated_text': translation_result['text'],
                'confidence': translation_result.get('confidence', 0.8),
                'detected_language': detected_lang,
                'processing_time': processing_time,
                'engine_used': translation_result.get('engine', 'unknown'),
                'original_length': len(arabic_text),
                'translated_length': len(translation_result['text'])
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            processing_time = time.time() - start_time
            
            return {
                'translated_text': f"Translation error: {str(e)}",
                'confidence': 0.0,
                'detected_language': 'unknown',
                'processing_time': processing_time,
                'engine_used': 'error',
                'error': str(e)
            }
    
    def _preprocess_arabic_text(self, text: str) -> str:
        """
        Preprocess Arabic text for better translation
        
        Args:
            text (str): Raw Arabic text
            
        Returns:
            str: Preprocessed Arabic text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Handle Arabic text reshaping for proper display
        try:
            # Reshape Arabic text for proper rendering
            reshaped_text = arabic_reshaper.reshape(text)
            text = get_display(reshaped_text)
        except Exception as e:
            logger.warning(f"Arabic reshaping failed: {e}")
        
        # Normalize Arabic characters
        text = self._normalize_arabic_characters(text)
        
        # Remove excessive diacritics while preserving meaning
        text = self._clean_diacritics(text)
        
        return text
    
    def _normalize_arabic_characters(self, text: str) -> str:
        """Normalize Arabic characters for consistent translation"""
        # Common Arabic character normalizations
        normalizations = {
            'أ': 'ا',  # Alif with hamza to regular alif
            'إ': 'ا',  # Alif with hamza below to regular alif
            'آ': 'ا',  # Alif madda to regular alif
            'ة': 'ه',  # Taa marbouta to haa
            'ى': 'ي',  # Alif maqsura to yaa
        }
        
        for old_char, new_char in normalizations.items():
            text = text.replace(old_char, new_char)
        
        return text
    
    def _clean_diacritics(self, text: str) -> str:
        """Remove excessive diacritics while preserving meaning"""
        # Remove tashkeel (diacritical marks) but keep essential ones
        text = self.arabic_patterns['diacritics'].sub('', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of the input text"""
        # Simple Arabic detection based on character ranges
        arabic_chars = re.findall(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text)
        if len(arabic_chars) > len(text) * 0.3:  # If more than 30% are Arabic characters
            return 'ar'
        return 'unknown'
    
    def _translate_with_fallback(self, text: str) -> Dict[str, Any]:
        """Try multiple translation engines with fallback"""
        engines_to_try = ['google', 'fallback']
        
        for engine_name in engines_to_try:
            try:
                result = self.translation_engines[engine_name](text)
                if result and result.get('text'):
                    result['engine'] = engine_name
                    return result
            except Exception as e:
                logger.warning(f"Engine {engine_name} failed: {e}")
                continue
        
        # If all engines fail, return error
        return {
            'text': 'Translation service temporarily unavailable',
            'confidence': 0.0,
            'engine': 'none'
        }
    
    def _translate_google(self, text: str) -> Dict[str, Any]:
        """Translate using Google Translate API (simplified version)"""
        try:
            # Use a simple Google Translate API endpoint
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'ar',
                'tl': 'ur',
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            if data and len(data) > 0 and len(data[0]) > 0:
                translated_text = ''.join([item[0] for item in data[0] if item[0]])
                return {
                    'text': translated_text,
                    'confidence': 0.9
                }
            else:
                raise Exception("Invalid response format")
                
        except Exception as e:
            logger.error(f"Google translation failed: {e}")
            raise
    
    def _translate_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback translation using basic character mapping"""
        # Basic Arabic to Urdu character mapping for common words
        basic_mapping = {
            'مرحبا': 'ہیلو',
            'شكرا': 'شکریہ',
            'نعم': 'ہاں',
            'لا': 'نہیں',
            'ماء': 'پانی',
            'خبز': 'روٹی',
            'بيت': 'گھر',
            'كتاب': 'کتاب',
            'قلم': 'قلم',
            'مدرسة': 'اسکول',
            'طالب': 'طالب علم',
            'معلم': 'استاد',
            'صديق': 'دوست',
            'عائلة': 'خاندان',
            'أم': 'ماں',
            'أب': 'باپ',
            'أخ': 'بھائی',
            'أخت': 'بہن',
            'ابن': 'بیٹا',
            'بنت': 'بیٹی',
            'جديد': 'نیا',
            'قديم': 'پرانا',
            'كبير': 'بڑا',
            'صغير': 'چھوٹا',
            'جميل': 'خوبصورت',
            'قبيح': 'بدصورت',
            'سريع': 'تیز',
            'بطيء': 'آہستہ',
            'ساخن': 'گرم',
            'بارد': 'ٹھنڈا',
            'جوعان': 'بھوکا',
            'عطشان': 'پیاسا',
            'متعب': 'تھکا ہوا',
            'سعيد': 'خوش',
            'حزين': 'اداس',
            'غاضب': 'غصہ',
            'خائف': 'خوفزدہ',
            'آمن': 'محفوظ',
            'خطر': 'خطرہ',
            'صحة': 'صحت',
            'مرض': 'بیماری',
            'دواء': 'دوا',
            'طبيب': 'ڈاکٹر',
            'مستشفى': 'ہسپتال',
            'عملية': 'آپریشن',
            'جرح': 'زخم',
            'دم': 'خون',
            'عظم': 'ہڈی',
            'جلد': 'جلد',
            'عين': 'آنکھ',
            'أذن': 'کان',
            'أنف': 'ناک',
            'فم': 'منہ',
            'يد': 'ہاتھ',
            'رجل': 'پاؤں',
            'رأس': 'سر',
            'قلب': 'دل',
            'دماغ': 'دماغ',
            'رئة': 'پھیپھڑا',
            'كبد': 'جگر',
            'معدة': 'پیٹ',
            'كلى': 'گردہ',
            'مثانة': 'مثانہ',
            'عصب': 'عصب',
            'عضلة': 'پٹھا',
            'شعر': 'بال',
            'ظفر': 'ناخن',
            'سن': 'دانت',
            'لسان': 'زبان',
            'حلق': 'گلا',
            'صدر': 'سینہ',
            'ظهر': 'پیٹھ',
            'بطن': 'پیٹ',
            'خصر': 'کمر',
            'كتف': 'کندھا',
            'مرفق': 'کہنی',
            'ركبة': 'گھٹنا',
            'كاحل': 'ٹخنہ',
            'كف': 'ہتھیلی',
            'قدم': 'پاؤں کا تلوہ',
            'إصبع': 'انگلی',
            'شفة': 'ہونٹ',
            'ذقن': 'ٹھوڑی',
            'جبين': 'پیشانی',
            'حاجب': 'ابرو',
            'رموش': 'پلکیں',
            'خد': 'گال',
            'وجنة': 'رخسار',
            'فك': 'جبڑا',
            'عنق': 'گردن',
            'حنجرة': 'حنجرہ',
            'قصبة': 'سانس کی نالی',
            'شرايين': 'شریانیں',
            'أوردة': 'وریدیں',
            'عظام': 'ہڈیاں',
            'مفاصل': 'جوڑ',
            'أربطة': 'لیگامینٹس',
            'أوتار': 'ٹینڈنز',
            'غضاريف': 'کارٹلیج',
            'نخاع': 'مغز',
            'حبل شوكي': 'ریڑھ کی ہڈی',
            'جمجمة': 'کھوپڑی',
            'فقرات': 'مہرے',
            'ضلوع': 'پسلیاں',
            'قص': 'چھاتی کی ہڈی',
            'ترقوة': 'ہنسلی',
            'عظم العضد': 'بازو کی ہڈی',
            'كعبرة': 'زند',
            'زند': 'زند',
            'عظام الرسغ': 'کلائی کی ہڈیاں',
            'عظام اليد': 'ہاتھ کی ہڈیاں',
            'عظام القدم': 'پاؤں کی ہڈیاں',
            'عظام الساق': 'پنڈلی کی ہڈیاں',
            'عظم الفخذ': 'ران کی ہڈی',
            'عظم الحوض': 'کمر کی ہڈی',
            'عظم العجز': 'کمر کی ہڈی',
            'عظم العصعص': 'دم کی ہڈی',
            'عظام الجمجمة': 'کھوپڑی کی ہڈیاں',
            'عظام الوجه': 'چہرے کی ہڈیاں',
            'عظام الأنف': 'ناک کی ہڈیاں',
            'عظام الأذن': 'کان کی ہڈیاں',
            'عظام الفك': 'جبڑے کی ہڈیاں',
            'عظام الأسنان': 'دانت کی ہڈیاں',
            'عظام اللسان': 'زبان کی ہڈیاں',
            'عظام الحلق': 'گلے کی ہڈیاں',
            'عظام الصدر': 'سینے کی ہڈیاں',
            'عظام البطن': 'پیٹ کی ہڈیاں',
            'عظام الظهر': 'پیٹھ کی ہڈیاں',
            'عظام الأطراف': 'ہاتھ پاؤں کی ہڈیاں',
            'عظام الرأس': 'سر کی ہڈیاں',
            'عظام العنق': 'گردن کی ہڈیاں',
            'عظام الكتف': 'کندھے کی ہڈیاں',
            'عظام الذراع': 'بازو کی ہڈیاں',
            'عظام الساعد': 'پہنچے کی ہڈیاں',
            'عظام اليد': 'ہاتھ کی ہڈیاں',
            'عظام الأصابع': 'انگلیوں کی ہڈیاں',
            'عظام الفخذ': 'ران کی ہڈیاں',
            'عظام الساق': 'پنڈلی کی ہڈیاں',
            'عظام القدم': 'پاؤں کی ہڈیاں',
            'عظام الأصابع القدم': 'پاؤں کی انگلیوں کی ہڈیاں',
            'عظام الكاحل': 'ٹخنے کی ہڈیاں',
            'عظام الركبة': 'گھٹنے کی ہڈیاں',
            'عظام الحوض': 'کمر کی ہڈیاں',
            'عظام العمود الفقري': 'ریڑھ کی ہڈی',
            'عظام القفص الصدري': 'سینے کی پسلیاں',
            'أهلا وسهلا': 'خوش آمدید',
            'مع السلامة': 'اللہ حافظ',
            'صباح الخير': 'صبح بخیر',
            'مساء الخير': 'شام بخیر',
            'كيف حالك': 'آپ کیسے ہیں',
            'أنا بخير': 'میں ٹھیک ہوں',
            'شكرا لك': 'آپ کا شکریہ',
            'عفوا': 'معاف کیجیے',
            'من فضلك': 'براہ کرم',
            'عذراً': 'معذرت',
            'ممتاز': 'بہترین',
            'جيد': 'اچھا',
            'سيء': 'برا',
            'صحيح': 'درست',
            'خطأ': 'غلط',
            'ممكن': 'ممکن',
            'مستحيل': 'ناممکن',
            'سهل': 'آسان',
            'صعب': 'مشکل',
            'قريب': 'قریب',
            'بعيد': 'دور',
            'فوق': 'اوپر',
            'تحت': 'نیچے',
            'يمين': 'دائیں',
            'يسار': 'بائیں',
            'امام': 'آگے',
            'خلف': 'پیچھے',
            'داخل': 'اندر',
            'خارج': 'باہر',
            'فوق': 'اوپر',
            'تحت': 'نیچے',
            'قبل': 'پہلے',
            'بعد': 'بعد',
            'الآن': 'اب',
            'غدا': 'کل',
            'أمس': 'کل',
            'اليوم': 'آج',
            'الليلة': 'آج رات',
            'صباحا': 'صبح',
            'مساء': 'شام',
            'ظهرا': 'دوپہر',
            'ليلا': 'رات',
            'ساعة': 'گھنٹہ',
            'دقيقة': 'منٹ',
            'ثانية': 'سیکنڈ',
            'سنة': 'سال',
            'شهر': 'مہینہ',
            'اسبوع': 'ہفتہ',
            'يوم': 'دن',
            'شهر': 'مہینہ',
            'فصل': 'موسم',
            'ربيع': 'بہار',
            'صيف': 'گرمی',
            'خريف': 'خزاں',
            'شتاء': 'سردی'
        }
        
        # Try to find exact matches first
        translated_text = text
        for arabic_word, urdu_word in basic_mapping.items():
            if arabic_word in translated_text:
                translated_text = translated_text.replace(arabic_word, urdu_word)
        
        # If no translation found, return original with note
        if translated_text == text:
            return {
                'text': f"[Translation not available] {text}",
                'confidence': 0.3
            }
        
        return {
            'text': translated_text,
            'confidence': 0.6
        }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return {
            'ar': 'Arabic',
            'ur': 'Urdu'
        }
    
    def get_translation_stats(self) -> Dict[str, Any]:
        """Get translation service statistics"""
        return {
            'engines_available': list(self.translation_engines.keys()),
            'supported_languages': self.get_supported_languages(),
            'service_status': 'operational'
        }