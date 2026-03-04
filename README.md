# Fake News Detection Project

## 📊 Project Overview

A complete machine learning web application to detect fake news from text or URLs. The project includes:
- **Backend**: Flask API with ML model (Support Vector Machine - 99.0% accuracy)
- **Frontend**: React + TypeScript with shadcn-ui and Tailwind CSS

## 🏆 Model Comparison Results

*Note: Models were recently retrained using advanced cleaning techniques to strip dataset-specific publisher artifacts (e.g. "WASHINGTON (Reuters) - "), forcing the models to evaluate actual linguistic structure rather than memorizing publisher names. The new unbiased performance metrics are below.*

| Rank | Model | Accuracy |
|------|-------|----------|
| 🥇 1 | **SVM (Linear)** | **99.00%** |
| 🥈 2 | Random Forest | 98.71% |
| 🥉 3 | Logistic Regression | 98.63% |
| 4 | Gradient Boosting | 97.54% |
| 5 | Naive Bayes (Multinomial) | 95.00% |
| 6 | Decision Tree | 94.87% |
| 7 | K-Nearest Neighbors | 90.21% |

## 📁 Project Structure

```
news-detection/
├── backend/
│   ├── app.py              # Flask API
│   ├── fake_news_detection.py  # Model training
│   ├── fake_news_model.pkl     # Trained model
│   ├── requirements.txt        # Python dependencies
│   ├── True.csv           # True news dataset
│   └── Fake.csv           # Fake news dataset
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── lib/           # Utilities & API
│   │   └── hooks/         # Custom React hooks
│   ├── api/               # Vercel serverless API
│   ├── package.json       # Node dependencies
│   └── vercel.json       # Vercel config
└── README.md
```

## 🚀 How to Run Locally

### Backend (Flask API)

```
bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend (React)

```
bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:8080`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/detect` | Detect fake news (single text) |
| POST | `/api/detect-url` | Detect fake news from URL |
| POST | `/api/detect-batch` | Detect fake news (multiple texts) |

### Example Request

```
bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news article text here"}'
```

### Example Response

```json
{
  "result": "FAKE",
  "is_fake": true,
  "confidence": 98.5,
  "confidence_fake": 98.5,
  "confidence_real": 1.5,
  "explanation": "Our AI detected sensationalist language...",
  "model_used": "SVM (Linear)",
  "model_accuracy": 99.00
}
```

## 🌐 Deploy to Vercel

### Option 1: Deploy Frontend + Serverless API

```
bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --yes
```

### Option 2: Separate Deployments

- **Frontend**: Deploy the `frontend` folder to Vercel, Netlify, or any static hosting
- **Backend**: Deploy to Render, Railway, or PythonAnywhere

## 🔧 Features

- ✅ Text-based fake news detection
- ✅ URL-based fake news detection
- ✅ Batch processing for multiple articles
- ✅ Confidence scores with explanations
- ✅ Real-time health monitoring
- ✅ Modern, responsive UI
- ✅ Dark/Light theme support

## 🛠️ Technologies Used

### Backend
- Python 3.x
- Flask + Flask-CORS
- scikit-learn (Random Forest)
- pandas, numpy
- BeautifulSoup4 (for URL extraction)

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Framer Motion

## 📝 Requirements

### Backend
```
flask>=2.3.0
flask-cors>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

### Frontend
```
node.js >= 18
npm >= 9
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes.

---

**Note**: The trained model (`fake_news_model.pkl`) is already included. To retrain, run `python fake_news_detection.py` in the backend folder.
