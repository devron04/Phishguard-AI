# 🛡️ PhishGuard AI: AI-Based Phishing Detection System

A high-fidelity, real-time phishing and spam detection system powered by Machine Learning. This project features a **FastAPI** backend and a premium **Glassmorphism** web dashboard.

---

## 🚀 Features
- **AI Core**: Uses TF-IDF Vectorization and Random Forest classification for high-accuracy detection.
- **Deep Phrase Analysis**: Trained on modern phishing patterns to catch sophisticated "bank account" and "investment" scams.
- **Modern UI**: A sleek, cybersecurity-inspired dashboard with smooth animations and hover effects.
- **Session History**: Track and manage your recent checks with an integrated deletion feature.

## 📁 Project Structure
```text
/ai phissing detector
├── backend/
│   ├── main.py             # FastAPI Server
│   ├── train_model.py       # ML Training Script
│   ├── phishing_model.pkl   # Trained Model Pipeline
│   └── requirements.txt    # Backend Dependencies
└── frontend/
    ├── index.html          # Web Interface
    ├── style.css           # UI Styling
    ├── script.js           # Frontend Logic
    └── background.png      # Branding Asset
```

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Retrain the model:
   ```bash
   python train_model.py
   ```
4. Start the server:
   ```bash
   python main.py
   ```

### 3. Frontend Setup
Simply open `frontend/index.html` in any modern web browser.

---

## 🧠 Model Information
- **Dataset**: Built using the UCI SMS Spam Collection supplemented with modern email phishing data.
- **Architecture**: Scikit-learn Pipeline with `RandomForestClassifier`.
- **Accuracy**: ~98.9% on test data.
- 
## 🔒 Security Note
This project is designed for educational and research purposes only.  
Do not use it as the sole protection layer for sensitive or production environments.

## 🤝 Contribution
Designed as a professional-grade college project/submission. Pull requests and feedback are welcome!
