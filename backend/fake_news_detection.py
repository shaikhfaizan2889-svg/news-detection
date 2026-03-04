"""
Fake News Detection Project
===========================
This project implements multiple machine learning models to detect fake news
from True.csv and Fake.csv datasets.

Models included:
- Logistic Regression
- Naive Bayes (Multinomial)
- Support Vector Machine (SVM)
- Random Forest
- Decision Tree
- Gradient Boosting
- XGBoost (if available)
- K-Nearest Neighbors
"""

import pandas as pd
import numpy as np
import re
import string
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import time

# Try to import XGBoost
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available. Proceeding without it.")

print("=" * 60)
print("FAKE NEWS DETECTION PROJECT")
print("=" * 60)

# =============================================================================
# 1. DATA LOADING
# =============================================================================
print("\n[1] Loading Data...")

# Load datasets
true_df = pd.read_csv('True.csv')
fake_df = pd.read_csv('Fake.csv')

print(f"   True News samples: {len(true_df)}")
print(f"   Fake News samples: {len(fake_df)}")

# =============================================================================
# 2. DATA PREPROCESSING
# =============================================================================
print("\n[2] Preprocessing Data...")

# Add labels (1 = True, 0 = Fake)
true_df['label'] = 1
fake_df['label'] = 0

# Combine datasets
df = pd.concat([true_df, fake_df], ignore_index=True)

# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"   Total samples: {len(df)}")
print(f"   True News: {(df['label'] == 1).sum()}")
print(f"   Fake News: {(df['label'] == 0).sum()}")

# =============================================================================
# 3. TEXT CLEANING
# =============================================================================
print("\n[3] Cleaning Text...")

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    
    # Remove datelines (e.g., "WASHINGTON (Reuters) - " or "LONDON (Reuters) -")
    text = re.sub(r'^.*?\(.*?\)\s*-\s*', '', text)
    
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

# Apply text cleaning
df['clean_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
df['clean_text'] = df['clean_text'].apply(clean_text)

# Remove empty texts
df = df[df['clean_text'].str.len() > 10].reset_index(drop=True)
print(f"   Samples after cleaning: {len(df)}")

# =============================================================================
# 4. FEATURE EXTRACTION
# =============================================================================
print("\n[4] Extracting Features (TF-IDF)...")

# Prepare features and labels
X = df['clean_text']
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")

# TF-IDF Vectorization
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    stop_words='english'
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print(f"   Feature dimensions: {X_train_tfidf.shape[1]}")

# =============================================================================
# 5. MODEL TRAINING AND EVALUATION
# =============================================================================
print("\n[5] Training and Evaluating Models...")
print("=" * 60)

# Dictionary to store results
results = {}

def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """Train and evaluate a model"""
    print(f"\nTraining {name}...")
    start_time = time.time()
    
    # Train
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Predict
    start_pred = time.time()
    y_pred = model.predict(X_test)
    pred_time = time.time() - start_pred
    
    # Evaluate
    accuracy = accuracy_score(y_test, y_pred)
    
    # Store results
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'predictions': y_pred,
        'train_time': train_time,
        'pred_time': pred_time
    }
    
    print(f"   ✓ {name} - Accuracy: {accuracy:.4f} | Train Time: {train_time:.2f}s | Pred Time: {pred_time:.4f}s")
    
    return accuracy

# Model 1: Logistic Regression
lr_model = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
evaluate_model("Logistic Regression", lr_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 2: Multinomial Naive Bayes
nb_model = MultinomialNB(alpha=0.1)
evaluate_model("Naive Bayes (Multinomial)", nb_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 3: Support Vector Machine
svm_model = LinearSVC(C=1.0, random_state=42, max_iter=2000)
evaluate_model("SVM (Linear)", svm_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 4: Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
evaluate_model("Random Forest", rf_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 5: Decision Tree
dt_model = DecisionTreeClassifier(random_state=42, max_depth=20)
evaluate_model("Decision Tree", dt_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 6: Gradient Boosting
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)
evaluate_model("Gradient Boosting", gb_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 7: K-Nearest Neighbors
knn_model = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
evaluate_model("K-Nearest Neighbors", knn_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# Model 8: XGBoost (if available)
if XGBOOST_AVAILABLE:
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss',
        n_jobs=-1
    )
    evaluate_model("XGBoost", xgb_model, X_train_tfidf, X_test_tfidf, y_train, y_test)

# =============================================================================
# 6. RESULTS COMPARISON
# =============================================================================
print("\n" + "=" * 60)
print("MODEL COMPARISON RESULTS")
print("=" * 60)

# Create results dataframe
results_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': [results[m]['accuracy'] for m in results],
    'Train Time (s)': [results[m]['train_time'] for m in results],
    'Prediction Time (s)': [results[m]['pred_time'] for m in results]
})

# Sort by accuracy
results_df = results_df.sort_values('Accuracy', ascending=False).reset_index(drop=True)

print("\n📊 Accuracy Ranking:")
print("-" * 60)
for i, row in results_df.iterrows():
    rank = i + 1
    model_name = row['Model']
    accuracy = row['Accuracy']
    bar = '█' * int(accuracy * 50)
    print(f"  {rank}. {model_name:25s} | {accuracy:.4f} | {bar}")

# Best model
best_model_name = results_df.iloc[0]['Model']
best_accuracy = results_df.iloc[0]['Accuracy']

print("\n" + "=" * 60)
print(f"🏆 BEST MODEL: {best_model_name}")
print(f"   Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
print("=" * 60)

# =============================================================================
# 7. DETAILED EVALUATION OF BEST MODEL
# =============================================================================
print(f"\n[6] Detailed Evaluation of {best_model_name}...")
print("-" * 60)

best_predictions = results[best_model_name]['predictions']

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, best_predictions, target_names=['Fake', 'True']))

# Confusion Matrix
cm = confusion_matrix(y_test, best_predictions)
print("Confusion Matrix:")
print(f"   True Negatives (Fake correctly identified):  {cm[0][0]}")
print(f"   False Positives (Fake predicted as True):  {cm[0][1]}")
print(f"   False Negatives (True predicted as Fake):  {cm[1][0]}")
print(f"   True Positives (True correctly identified): {cm[1][1]}")

# =============================================================================
# 8. SAVE RESULTS
# =============================================================================
print("\n[7] Saving Results...")

# Save comparison results
results_df.to_csv('model_comparison.csv', index=False)
print("   ✓ Model comparison saved to 'model_comparison.csv'")

# =============================================================================
# 8. SAVE BEST MODEL
# =============================================================================
print("\n[8] Saving Best Model...")

# Get the best model
best_model = results[best_model_name]['model']

# Save the model using pickle
model_data = {
    'model': best_model,
    'model_name': best_model_name,
    'tfidf': tfidf,
    'accuracy': best_accuracy
}

# Save model and vectorizer to pickle file
with open('fake_news_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print(f"   ✓ Best model ({best_model_name}) saved to 'fake_news_model.pkl'")
print(f"   ✓ TF-IDF vectorizer saved to 'fake_news_model.pkl'")

# =============================================================================
# 9. DEMONSTRATE SAVED MODEL
# =============================================================================
print("\n[9] Demonstrating Saved Model...")

# Load the saved model
print("   Loading saved model...")
with open('fake_news_model.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

loaded_model = loaded_data['model']
loaded_tfidf = loaded_data['tfidf']
loaded_model_name = loaded_data['model_name']

print(f"   ✓ Model loaded: {loaded_model_name}")

# Test predictions with sample news
print("\n   Testing with sample news articles:")
print("-" * 60)

sample_news = [
    "Trump says he will build a wall on the border",
    "President Obama meets with world leaders to discuss climate change",
    "BREAKING: Scientists discover cure for cancer",
    "Obama administration announces new economic policies",
    "Scientists discover new species in Amazon rainforest"
]

for news in sample_news:
    # Clean the text
    cleaned = clean_text(news)
    # Transform using loaded TF-IDF
    news_tfidf = loaded_tfidf.transform([cleaned])
    # Predict
    prediction = loaded_model.predict(news_tfidf)[0]
    
    if hasattr(loaded_model, "predict_proba"):
        probability = loaded_model.predict_proba(news_tfidf)[0]
    else:
        import math
        decision = loaded_model.decision_function(news_tfidf)[0]
        prob = 1 / (1 + math.exp(-decision))
        probability = [1 - prob, prob]
    
    label = "TRUE" if prediction == 1 else "FAKE"
    confidence = max(probability) * 100
    
    print(f"   News: {news[:50]}...")
    print(f"   Prediction: {label} (Confidence: {confidence:.2f}%)")
    print()

print("-" * 60)
print("   ✓ Model demonstration complete!")

# =============================================================================
# 10. SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("PROJECT SUMMARY")
print("=" * 60)
print(f"""
📌 Dataset Statistics:
   - Total samples: {len(df)}
   - True news: {(df['label'] == 1).sum()}
   - Fake news: {(df['label'] == 0).sum()}
   
📌 Feature Extraction:
   - Method: TF-IDF Vectorization
   - Max features: 10,000
   - N-gram range: (1, 2)
   
📌 Models Evaluated: {len(results)}
   
📌 Best Model: {best_model_name}
   - Test Accuracy: {best_accuracy:.4f}
   
📌 Output Files:
   - model_comparison.csv
   - fake_news_model.pkl
""")

print("=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 60)
