import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import os

def train():
    print("Fetching dataset...")
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    
    # Load dataset (tab separated: label, message)
    df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])
    
    # --- ADDING MODERN PHISHING DATA (HARDENED) ---
    modern_phishing = [
        "URGENT: Your bank account has been compromised. Log in here to secure it.",
        "FREE INVESTMENT ADVICE! Earn $5000 a week from home with this simple trick. Guaranteed results!",
        "Verify your identity to avoid account suspension. Click here.",
        "Notification of suspicious activity on your account. Please log in to confirm.",
        "New sign-in from an unknown device. If this wasn't you, click here to secure your account.",
        "Your subscription has expired. Update your billing info now to avoid service interruption.",
        "You have a pending refund of $450. Click to claim your money.",
        "Urgent: Action required on your Amazon account. Security alert.",
        "Payroll department: Your direct deposit information has been updated. If this was not you, contact us immediately.",
        "Final Notice: Your tax return has been flagged for audit. Submit missing documents here.",
        "Click here to claim your $500 reward. Limited time offer!",
        "Account Security Alert: Weird login detected. Use this link to protect your data.",
        "You have won a free iPhone! Click to provide your shipping details."
    ]
    
    # AGGRESSIVE AUGMENTATION: Multiply these examples 100 times to force balance
    modern_phishing_expanded = modern_phishing * 100
    
    # Create a dataframe for modern phishing
    df_modern = pd.DataFrame({
        'label': ['spam'] * len(modern_phishing_expanded),
        'message': modern_phishing_expanded
    })
    
    # Combine datasets
    df = pd.concat([df, df_modern], ignore_index=True)
    
    # Convert label to numeric
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    
    X = df['message']
    y = df['label_num']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training Hardened Model on {len(X_train)} samples...")
    
    # Create an improved pipeline
    # 1. TfidfVectorizer without stop_words to keep critical phishing words
    # 2. RandomForestClassifier for better pattern matching
    model_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(
            lowercase=True, 
            ngram_range=(1, 2), 
            max_features=5000
        )),
        ('classifier', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
    ])
    
    # Train
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate
    score = model_pipeline.score(X_test, y_test)
    print(f"Hardened model accuracy: {score:.2%}")
    
    # Save the pipeline
    print("Saving hardened model pipeline...")
    joblib.dump(model_pipeline, 'phishing_model.pkl')
    print("Done!")

if __name__ == "__main__":
    train()
