from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import time
import uuid

app = FastAPI(title="AI Phishing Detector API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model pipeline
MODEL_PATH = 'phishing_model.pkl'
model = None

def get_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            raise Exception("Model file not found. Please run train_model.py first.")
    return model

class MessageRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    is_spam: bool
    timestamp: float

# In-memory history (for demo purposes)
history = []

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: MessageRequest):
    try:
        clf = get_model()
        
        # Predict
        prediction = clf.predict([request.text])[0]
        # Get probabilities
        probs = clf.predict_proba([request.text])[0]
        confidence = float(max(probs))
        
        is_spam = bool(prediction == 1)
        label = "Spam/Phishing" if is_spam else "Safe/Legit"
        
        result = {
            "label": label,
            "confidence": confidence,
            "is_spam": is_spam,
            "timestamp": time.time()
        }
        
        # Add to history with a unique ID
        item_id = str(uuid.uuid4())
        history.insert(0, {
            **result, 
            "id": item_id,
            "text": request.text[:100] + "..." if len(request.text) > 100 else request.text
        })
        if len(history) > 10: # Keep last 10
            history.pop()
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    return history

@app.delete("/history/{item_id}")
async def delete_history_item(item_id: str):
    global history
    history = [item for item in history if item.get("id") != item_id]
    return {"status": "deleted"}

@app.get("/")
async def root():
    return {"status": "online", "model_loaded": os.path.exists(MODEL_PATH)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
