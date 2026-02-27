"""
Flask API for Fake News Detection
================================
This API provides endpoints for detecting fake news using the trained ML model.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import string
import numpy as np
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)

# Load the trained model and TF-IDF vectorizer
MODEL_PATH = 'fake_news_model.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    tfidf = model_data['tfidf']
    model_name = model_data['model_name']
    model_accuracy = model_data['accuracy']
    
    print(f"Model loaded successfully: {model_name}")
    print(f"Model accuracy: {model_accuracy:.4f}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    tfidf = None


def clean_text(text):
    """Clean and preprocess text data (same as training)"""
    if not text or pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def fetch_url_content(url):
    """Fetch and extract text content from a URL"""
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Try to find main article content
        article = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('article|content|main'))
        
        if article:
            text = article.get_text(separator=' ', strip=True)
        else:
            # Fallback to body text
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 chars for analysis
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing URL content: {str(e)}")



import pandas as pd


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_name': model_name if model else None,
        'model_accuracy': model_accuracy if model else None
    })


@app.route('/api/detect', methods=['POST'])
def detect_fake_news():
    """Detect fake news from provided text"""
    if model is None or tfidf is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    # Get the news text from request
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({
            'error': 'Please provide news text to analyze.'
        }), 400
    
    news_text = data['text'].strip()
    
    if not news_text:
        return jsonify({
            'error': 'Please provide news text to analyze.'
        }), 400
    
    # Clean the text
    cleaned_text = clean_text(news_text)
    
    # Transform using TF-IDF
    text_tfidf = tfidf.transform([cleaned_text])
    
    # Make prediction
    prediction = model.predict(text_tfidf)[0]
    probabilities = model.predict_proba(text_tfidf)[0]
    
    # Get confidence scores (as percentages, capped at 100)
    confidence_fake = min(float(probabilities[0]) * 100, 100.0)
    confidence_real = min(float(probabilities[1]) * 100, 100.0)
    
    # Determine result
    is_fake = bool(prediction == 0)
    result_label = "FAKE" if is_fake else "REAL"
    confidence = max(confidence_fake, confidence_real)
    
    # Generate explanation
    explanation = generate_explanation(news_text.lower(), is_fake, confidence)
    
    return jsonify({
        'result': result_label,
        'is_fake': is_fake,
        'confidence': round(confidence, 2),
        'confidence_fake': round(confidence_fake, 2),
        'confidence_real': round(confidence_real, 2),
        'explanation': explanation,
        'model_used': model_name,
        'model_accuracy': model_accuracy
    })


@app.route('/api/detect-url', methods=['POST'])
def detect_fake_news_from_url():
    """Detect fake news from a URL"""
    if model is None or tfidf is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({
            'error': 'Please provide a URL to analyze.'
        }), 400
    
    url = data['url'].strip()
    
    if not url:
        return jsonify({
            'error': 'Please provide a valid URL.'
        }), 400
    
    try:
        # Fetch content from URL
        news_text = fetch_url_content(url)
        
        if not news_text or len(news_text) < 50:
            return jsonify({
                'error': 'Could not extract sufficient text content from the URL.'
            }), 400
        
        # Clean the text
        cleaned_text = clean_text(news_text)
        
        # Transform using TF-IDF
        text_tfidf = tfidf.transform([cleaned_text])
        
        # Make prediction
        prediction = model.predict(text_tfidf)[0]
        probabilities = model.predict_proba(text_tfidf)[0]
        
        # Get confidence scores (as percentages, capped at 100)
        confidence_fake = min(float(probabilities[0]) * 100, 100.0)
        confidence_real = min(float(probabilities[1]) * 100, 100.0)
        
        # Determine result
        is_fake = bool(prediction == 0)
        result_label = "FAKE" if is_fake else "REAL"
        confidence = max(confidence_fake, confidence_real)
        
        # Generate explanation
        explanation = generate_explanation(news_text.lower(), is_fake, confidence)
        
        return jsonify({
            'result': result_label,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'confidence_fake': round(confidence_fake, 2),
            'confidence_real': round(confidence_real, 2),
            'explanation': explanation,
            'url': url,
            'extracted_text_preview': news_text[:200] + '...' if len(news_text) > 200 else news_text,
            'model_used': model_name,
            'model_accuracy': model_accuracy
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400


@app.route('/api/detect-batch', methods=['POST'])
def detect_fake_news_batch():

    """Detect fake news for multiple texts"""
    if model is None or tfidf is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    data = request.get_json()
    
    if not data or 'texts' not in data:
        return jsonify({
            'error': 'Please provide texts array to analyze.'
        }), 400
    
    texts = data['texts']
    results = []
    
    for news_text in texts:
        if not news_text or not news_text.strip():
            continue
            
        cleaned_text = clean_text(news_text)
        text_tfidf = tfidf.transform([cleaned_text])
        prediction = model.predict(text_tfidf)[0]
        probabilities = model.predict_proba(text_tfidf)[0]
        
        is_fake = bool(prediction == 0)
        confidence = max(float(probabilities[0]), float(probabilities[1])) * 100
        
        results.append({
            'text': news_text[:100] + '...' if len(news_text) > 100 else news_text,
            'result': "FAKE" if is_fake else "REAL",
            'is_fake': is_fake,
            'confidence': round(confidence, 2)
        })
    
    return jsonify({
        'results': results,
        'total_analyzed': len(results)
    })


def generate_explanation(text, is_fake, confidence):
    """Generate explanation for the prediction"""
    
    # Fake news indicators
    fake_indicators = [
        'breaking:', 'shocking', "you won't believe", 'secret', "they don't want you to know",
        'exposed', 'conspiracy', 'aliens', 'miracle cure', 'government hiding', 'full disclosure',
        '!!!', 'share before deleted', 'doctors hate', 'one weird trick'
    ]
    
    # Real news indicators
    real_indicators = [
        'according to', 'study shows', 'research', 'scientists', 'university',
        'published', 'peer-reviewed', 'official statement', 'confirmed', 'report',
        'analysis', 'data suggests', 'experts say'
    ]
    
    if is_fake:
        reasons = []
        if any(indicator in text for indicator in ['breaking:', '!!!']):
            reasons.append('sensationalist language')
        if any(indicator in text for indicator in ["you won't believe", 'shocking', 'wow']):
            reasons.append('clickbait phrases')
        if any(indicator in text for indicator in ['aliens', 'conspiracy', 'secret']):
            reasons.append('unverifiable claims')
        if any(indicator in text for indicator in ["government hiding", "they don't want"]):
            reasons.append('conspiracy rhetoric')
        
        # Check for ALL CAPS
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
        if caps_ratio > 0.3:
            reasons.append('excessive capitalization')
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 2:
            reasons.append('excessive punctuation')
        
        if not reasons:
            reasons.append('patterns commonly found in misleading content')
        
        return f"Our AI detected {', '.join(reasons)}. This content exhibits characteristics often associated with misinformation. We recommend verifying with trusted news sources before sharing."
    else:
        reasons = []
        if any(indicator in text for indicator in ['study', 'research']):
            reasons.append('references to scientific research')
        if any(indicator in text for indicator in ['according to', 'official']):
            reasons.append('attribution to sources')
        if any(indicator in text for indicator in ['scientists', 'experts']):
            reasons.append('expert citations')
        
        if not reasons:
            reasons.append('neutral reporting patterns')
        
        return f"Our AI detected {', '.join(reasons)}. This content appears to follow journalistic standards typical of credible reporting. However, always cross-reference with multiple reliable sources."


if __name__ == '__main__':
    print("=" * 60)
    print("FAKE NEWS DETECTION API")
    print("=" * 60)
    print("Starting server...")
    print("API available at: http://localhost:5000")
    print("Endpoints:")
    print("  - GET  /api/health       - Health check")
    print("  - POST /api/detect       - Detect fake news (single text)")
    print("  - POST /api/detect-url   - Detect fake news from URL")
    print("  - POST /api/detect-batch - Detect fake news (multiple texts)")
    print("=" * 60)

    app.run(debug=True, port=5000)
