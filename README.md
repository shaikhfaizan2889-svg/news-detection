# Fake News Detection Project

## 📊 Project Overview

This project implements a complete machine learning pipeline to detect fake news from True and Fake news datasets.

## 🏆 Model Comparison Results

| Rank | Model | Accuracy | Train Time (s) | Prediction Time (s) |
|------|-------|----------|----------------|---------------------|
| 🥇 1 | **Random Forest** | **99.73%** | 13.17 | 0.163 |
| 🥈 2 | Gradient Boosting | 99.60% | 487.44 | 0.117 |
| 🥉 3 | Decision Tree | 99.54% | 22.20 | 0.018 |
| 4 | SVM (Linear) | 99.47% | 1.29 | 0.010 |
| 5 | Logistic Regression | 99.01% | 0.71 | 0.004 |
| 6 | Naive Bayes (Multinomial) | 95.22% | 0.04 | 0.011 |
| 7 | K-Nearest Neighbors | 89.44% | 0.33 | 35.70 |

## 🏆 Best Model: Random Forest

- **Accuracy**: 99.73%
- **Training Time**: 13.17 seconds
- **Prediction Time**: 0.163 seconds

## 📁 Files

- `fake_news_detection.py` - Main Python script
- `True.csv` - Dataset containing true news articles
- `Fake.csv` - Dataset containing fake news articles
- `model_comparison.csv` - Model comparison results
- `README.md` - This file

## 🚀 How to Run

```
bash
python fake_news_detection.py
```

## 📈 Dataset Statistics

- **Total samples**: ~44,910
- **True News**: 21,419
- **Fake News**: 23,491
- **Features**: TF-IDF (10,000 features)
- **Train/Test Split**: 80/20

## 🔧 Features Used

- **Text Cleaning**: Lowercase, URL removal, HTML removal, punctuation removal
- **Feature Extraction**: TF-IDF Vectorization
  - Max features: 10,000
  - N-gram range: (1, 2)
  - Min document frequency: 2
  - Max document frequency: 0.95
  - Stop words: English

## 🧠 Models Implemented

1. **Logistic Regression** - Linear model, 99.01% accuracy
2. **Naive Bayes (Multinomial)** - Probabilistic model, 95.22% accuracy
3. **SVM (Linear)** - Support Vector Machine, 99.47% accuracy
4. **Random Forest** - Ensemble method, 99.73% accuracy ⭐ BEST
5. **Decision Tree** - Tree-based model, 99.54% accuracy
6. **Gradient Boosting** - Boosting method, 99.60% accuracy
7. **K-Nearest Neighbors** - Instance-based, 89.44% accuracy
8. **XGBoost** - Advanced boosting (if available)

## 📝 Requirements

- Python 3.x
- pandas
- numpy
- scikit-learn
- xgboost (optional)

## 📋 Conclusion

The **Random Forest** classifier achieved the best performance with **99.73% accuracy**, making it the recommended model for fake news detection in this dataset. It provides an excellent balance between accuracy and computational efficiency.
