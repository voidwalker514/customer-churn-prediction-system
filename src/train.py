import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb

def train_model():
    print("Loading data...")
    data_path = 'data/customer_churn_data.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} not found. Please run src/generate_data.py first.")
    
    df = pd.read_csv(data_path)
    
    # Feature Engineering / Selection
    X = df.drop(columns=['CustomerID', 'Churn'])
    y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # Identify numerical and categorical columns
    numerical_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'TotalCharges', 'SupportCalls']
    categorical_cols = ['Gender', 'ContractType', 'PaymentMethod']
    
    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Create the model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42))
    ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost Model...")
    model.fit(X_train, y_train)
    
    print("Evaluating Model...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    model_path = 'models/model.joblib'
    joblib.dump(model, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
