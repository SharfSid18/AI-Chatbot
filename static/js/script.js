// Global variables
let isTranslating = false;

// DOM elements
const arabicInput = document.getElementById('arabicInput');
const urduOutput = document.getElementById('urduOutput');
const translateBtn = document.getElementById('translateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const inputCharCount = document.getElementById('inputCharCount');
const outputCharCount = document.getElementById('outputCharCount');

// Translation details elements
const engineUsed = document.getElementById('engineUsed');
const confidence = document.getElementById('confidence');
const processingTime = document.getElementById('processingTime');
const detectedLanguage = document.getElementById('detectedLanguage');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add event listeners
    arabicInput.addEventListener('input', updateCharCount);
    urduOutput.addEventListener('input', updateOutputCharCount);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Initialize character counts
    updateCharCount();
    updateOutputCharCount();
    
    console.log('🚀 Arabic to Urdu Translation Agent initialized');
}

// Character counting functions
function updateCharCount() {
    const count = arabicInput.value.length;
    inputCharCount.textContent = count;
    
    // Update button state
    translateBtn.disabled = count === 0 || isTranslating;
}

function updateOutputCharCount() {
    const count = urduOutput.value.length;
    outputCharCount.textContent = count;
}

// Main translation function
async function translateText() {
    const text = arabicInput.value.trim();
    
    if (!text) {
        showNotification('Please enter some Arabic text to translate', 'error');
        return;
    }
    
    if (isTranslating) {
        return;
    }
    
    try {
        setTranslatingState(true);
        clearTranslationDetails();
        
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayTranslation(result);
            showNotification('Translation completed successfully!', 'success');
        } else {
            throw new Error(result.error || 'Translation failed');
        }
        
    } catch (error) {
        console.error('Translation error:', error);
        urduOutput.value = `Translation error: ${error.message}`;
        showNotification('Translation failed. Please try again.', 'error');
    } finally {
        setTranslatingState(false);
    }
}

// Display translation results
function displayTranslation(result) {
    urduOutput.value = result.translated;
    updateOutputCharCount();
    
    // Update translation details
    engineUsed.textContent = result.engine_used || 'Unknown';
    confidence.textContent = `${(result.confidence * 100).toFixed(1)}%`;
    processingTime.textContent = `${(result.processing_time * 1000).toFixed(0)}ms`;
    detectedLanguage.textContent = getLanguageName(result.detected_language);
    
    // Add success styling
    urduOutput.classList.add('success');
    setTimeout(() => {
        urduOutput.classList.remove('success');
    }, 2000);
}

// Clear translation details
function clearTranslationDetails() {
    engineUsed.textContent = '-';
    confidence.textContent = '-';
    processingTime.textContent = '-';
    detectedLanguage.textContent = '-';
}

// Set translating state
function setTranslatingState(translating) {
    isTranslating = translating;
    translateBtn.disabled = translating;
    
    if (translating) {
        translateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Translating...';
        loadingSpinner.style.display = 'block';
        urduOutput.value = 'Translating...';
        urduOutput.classList.add('loading');
    } else {
        translateBtn.innerHTML = '<i class="fas fa-arrow-right"></i> <span>Translate to Urdu</span>';
        loadingSpinner.style.display = 'none';
        urduOutput.classList.remove('loading');
    }
}

// Text control functions
function clearInput() {
    arabicInput.value = '';
    updateCharCount();
    showNotification('Input cleared', 'info');
}

function clearOutput() {
    urduOutput.value = '';
    updateOutputCharCount();
    clearTranslationDetails();
    showNotification('Output cleared', 'info');
}

async function pasteText() {
    try {
        const text = await navigator.clipboard.readText();
        arabicInput.value = text;
        updateCharCount();
        showNotification('Text pasted from clipboard', 'success');
    } catch (error) {
        showNotification('Failed to paste from clipboard', 'error');
    }
}

function copyTranslation() {
    const text = urduOutput.value;
    if (!text) {
        showNotification('No translation to copy', 'error');
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Translation copied to clipboard', 'success');
    }).catch(() => {
        // Fallback for older browsers
        urduOutput.select();
        document.execCommand('copy');
        showNotification('Translation copied to clipboard', 'success');
    });
}

// Load example text
function loadExample(text) {
    arabicInput.value = text;
    updateCharCount();
    showNotification('Example loaded', 'info');
    
    // Auto-translate after a short delay
    setTimeout(() => {
        translateText();
    }, 500);
}

// Keyboard shortcuts
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + Enter to translate
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        translateText();
    }
    
    // Ctrl/Cmd + Shift + C to copy translation
    if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'C') {
        event.preventDefault();
        copyTranslation();
    }
    
    // Ctrl/Cmd + Shift + V to paste
    if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'V') {
        event.preventDefault();
        pasteText();
    }
    
    // Escape to clear input
    if (event.key === 'Escape') {
        clearInput();
    }
}

// Utility functions
function getLanguageName(code) {
    const languages = {
        'ar': 'Arabic',
        'ur': 'Urdu',
        'en': 'English',
        'unknown': 'Unknown'
    };
    return languages[code] || code;
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    return icons[type] || 'fa-info-circle';
}

function getNotificationColor(type) {
    const colors = {
        'success': 'linear-gradient(135deg, #48bb78, #38a169)',
        'error': 'linear-gradient(135deg, #f56565, #e53e3e)',
        'warning': 'linear-gradient(135deg, #ed8936, #dd6b20)',
        'info': 'linear-gradient(135deg, #667eea, #764ba2)'
    };
    return colors[type] || colors.info;
}

// Modal functions
function showApiDocs() {
    const modal = document.getElementById('apiModal');
    modal.style.display = 'block';
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeApiModal();
        }
    });
}

function closeApiModal() {
    const modal = document.getElementById('apiModal');
    modal.style.display = 'none';
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification button {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 0;
        font-size: 0.9rem;
        opacity: 0.7;
        transition: opacity 0.3s ease;
    }
    
    .notification button:hover {
        opacity: 1;
    }
`;
document.head.appendChild(style);

// Health check function
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const result = await response.json();
        
        const statusBadge = document.querySelector('.status-badge');
        if (result.status === 'healthy') {
            statusBadge.className = 'status-badge online';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Online';
        } else {
            statusBadge.className = 'status-badge offline';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Offline';
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
}

// Periodic health check
setInterval(checkHealth, 30000); // Check every 30 seconds

// Export functions for global access
window.translateText = translateText;
window.clearInput = clearInput;
window.clearOutput = clearOutput;
window.pasteText = pasteText;
window.copyTranslation = copyTranslation;
window.loadExample = loadExample;
window.showApiDocs = showApiDocs;
window.closeApiModal = closeApiModal;