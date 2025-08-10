# Arabic to Urdu Translation Agent

A professional, AI-powered translation service that provides accurate translations from Arabic to Urdu. Built with modern web technologies and featuring a beautiful, responsive user interface.

## 🌟 Features

- **AI-Powered Translation**: Advanced machine learning algorithms for accurate translations
- **Professional UI/UX**: Modern, responsive design with intuitive user interface
- **Real-time Translation**: Fast and reliable translation service
- **Text Preprocessing**: Intelligent text cleaning and normalization
- **Character Counting**: Real-time character count for input and output
- **Copy & Download**: Easy copying and downloading of translations
- **Keyboard Shortcuts**: Quick access to common functions
- **Error Handling**: Comprehensive error handling and user feedback
- **Mobile Responsive**: Works perfectly on all devices
- **Accessibility**: Built with accessibility best practices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd arabic-urdu-translator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file and add your Google Translate API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Google Translate API (Optional)

For enhanced translation quality, you can use the Google Translate API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Cloud Translation API
4. Create credentials (API key)
5. Add the API key to your `.env` file

**Note**: The application works without an API key using the free googletrans library, but the API provides better accuracy and reliability.

## 📖 Usage

### Web Interface

1. **Enter Arabic Text**: Type or paste Arabic text in the input field
2. **Translate**: Click the "Translate" button or press `Ctrl/Cmd + Enter`
3. **View Results**: The Urdu translation will appear in the output field
4. **Copy/Download**: Use the buttons to copy or download the translation

### Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Translate text
- `Ctrl/Cmd + Shift + C`: Copy Urdu translation
- `Ctrl/Cmd + Shift + D`: Download translation

### API Usage

The application also provides a REST API:

```bash
# Translate text
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "مرحبا بالعالم"}'

# Health check
curl http://localhost:5000/health
```

## 🏗️ Architecture

### Backend (Flask)

- **app.py**: Main Flask application with translation logic
- **ArabicToUrduTranslator**: Core translation class with preprocessing and postprocessing
- **Error Handling**: Comprehensive error handling and logging
- **API Endpoints**: RESTful API for translation services

### Frontend (HTML/CSS/JavaScript)

- **Modern UI**: Responsive design with CSS Grid and Flexbox
- **Interactive Features**: Real-time character counting, auto-resize textareas
- **User Feedback**: Toast notifications and loading states
- **Accessibility**: ARIA labels and keyboard navigation

### Translation Pipeline

1. **Text Preprocessing**: Clean and normalize Arabic text
2. **Translation**: Use Google Translate API or googletrans library
3. **Postprocessing**: Clean and format Urdu output
4. **Validation**: Ensure translation quality and completeness

## 🔍 Technical Details

### Dependencies

- **Flask**: Web framework
- **googletrans**: Free translation library
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **flask-cors**: Cross-origin resource sharing

### Text Processing

- **Arabic Normalization**: Standardize Arabic characters
- **Whitespace Cleaning**: Remove extra spaces and formatting
- **Character Validation**: Ensure proper Arabic input
- **Output Formatting**: Clean and format Urdu text

### Error Handling

- **Network Errors**: Handle API failures gracefully
- **Input Validation**: Validate text length and content
- **Translation Errors**: Provide meaningful error messages
- **User Feedback**: Toast notifications for all actions

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

1. **Using Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker**
   ```bash
   docker build -t arabic-urdu-translator .
   docker run -p 5000:5000 arabic-urdu-translator
   ```

3. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export GOOGLE_TRANSLATE_API_KEY=your_api_key
   ```

## 📊 Performance

- **Translation Speed**: Average 1-3 seconds per translation
- **Text Length**: Supports up to 5000 characters per translation
- **Concurrent Users**: Handles multiple simultaneous translations
- **Memory Usage**: Optimized for low memory footprint

## 🔒 Security

- **Input Validation**: Sanitize all user inputs
- **Error Handling**: Prevent information leakage
- **CORS**: Configured for secure cross-origin requests
- **Environment Variables**: Secure API key management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Translate API for translation services
- Font Awesome for icons
- Inter font family for typography
- Flask community for the excellent web framework

## 📞 Support

For support and questions:

- Create an issue in the GitHub repository
- Check the documentation above
- Review the error logs for troubleshooting

## 🔄 Updates

Stay updated with the latest features and improvements:

```bash
git pull origin main
pip install -r requirements.txt
```

---

**Built with ❤️ for accurate Arabic to Urdu translations** 
