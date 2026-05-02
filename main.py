from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using XGBoost",
    version="1.0.0"
)

# Enable CORS for the frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input schema
class CustomerData(BaseModel):
    Age: int
    Gender: str
    TenureMonths: int
    ContractType: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float
    SupportCalls: int

# Global variable to hold the model
model = None

@app.on_event("startup")
def load_model():
    global model
    model_path = "models/model.joblib"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        print(f"Warning: Model not found at {model_path}. Please train the model first.")



@app.post("/predict")
def predict_churn(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Train the model first.")
        
    try:
        # Convert input data to pandas DataFrame
        data = pd.DataFrame([customer.dict()])
        
        # Predict churn probability
        probability = model.predict_proba(data)[0][1]
        
        # Predict class (0 or 1)
        prediction = int(model.predict(data)[0])
        
        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(float(probability), 4),
            "risk_level": "High" if probability > 0.7 else ("Medium" if probability > 0.4 else "Low")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Mount the frontend directory to serve the HTML dashboard at the root (/)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
