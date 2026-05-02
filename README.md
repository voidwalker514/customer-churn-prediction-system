# Customer Churn Prediction Model

## 1. Project Overview

**What is Customer Churn?**
Customer churn occurs when customers or subscribers stop doing business with a company or service. It is a critical metric for businesses with a subscription-based model. In this project, we treat churn prediction as a **binary classification problem** (1 = Churn, 0 = Retained).

**Why is Churn Prediction Important?**
- **Reduce Customer Loss:** Identifies at-risk customers early.
- **Improve Retention:** Allows businesses to proactively address customer pain points.
- **Increase Revenue:** Retaining existing customers is significantly cheaper than acquiring new ones.
- **Targeted Marketing:** Helps allocate retention budgets efficiently (e.g., offering discounts only to those likely to leave).

**Workflow:**
1. **Customer Data:** Collect demographics, account information, and usage metrics.
2. **Preprocessing:** Clean data, scale numerical features, and encode categorical features.
3. **Model:** Train an XGBoost classification algorithm.
4. **Churn Prediction:** Generate probability scores for customer churn.
5. **Business Insights:** Use feature importance to derive actionable retention strategies.

---

## 2. Tech Stack

This project uses an **Intermediate / Industry-Relevant** tech stack:
- **Programming Language:** Python 3.9+
- **Data Manipulation & Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, XGBoost
- **API Development:** FastAPI, Uvicorn
- **Data Visualization:** Matplotlib, Seaborn
- **Synthetic Data Generation:** Faker

This stack demonstrates a strong end-to-end understanding from data generation to deploying a machine learning model via an API.

---

## 3. Project Architecture

1. **Input:** Synthetic customer dataset containing Demographics (Age, Gender), Account Info (Tenure, Contract Type), and Usage Metrics (Monthly Charges, Support Calls).
2. **Processing:** 
   - Numerical data scaling using `StandardScaler`.
   - Categorical data encoding using `OneHotEncoder`.
   - Pipeline integration for seamless transformation.
3. **Model:** `XGBClassifier` optimized for tabular data classification.
4. **Output:** A JSON response from the FastAPI service containing the Churn Prediction (Yes/No), Churn Probability, and a Risk Level indicator (Low/Medium/High).

---

## 4. Virtual Simulation (Data Generation)

Since we do not have access to real proprietary company data, this project uses **Virtual Simulation** to generate a highly realistic dataset.
- The `src/generate_data.py` script uses the `Faker` library to simulate 5000 customer profiles.
- **Churn Logic Simulation:** We programmatically define churn behavior to mimic real-world patterns. For example, customers with "Month-to-month" contracts, short tenure (<12 months), and high support calls (>3) are assigned a statistically higher probability of churning.
- This creates realistic correlations that the machine learning model can learn from, perfectly simulating a real-world Data Science scenario.

---

## 5. Folder Structure

```
Customer-Churn-Prediction/
│
├── data/                  # Contains the generated customer_churn_data.csv
├── notebooks/             # Jupyter notebooks for EDA and Preprocessing
├── src/                   # Source code for data generation and model training
│   ├── generate_data.py
│   └── train.py
├── models/                # Saved joblib models
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── main.py                # FastAPI scoring service
```

---

## 6. Installation Guide

Follow these steps to set up the project on your local machine.

### Step 1: Clone the repository (or navigate to the folder)
```bash
cd "Customer-Churn-Prediction"
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 7. How to Run the Project Step-by-Step

### Phase 1: Generate the Data
Run the virtual simulation to create the synthetic dataset.
```bash
python src/generate_data.py
```
*Output: `Successfully generated 5000 records in data/customer_churn_data.csv`*

### Phase 2: Exploratory Data Analysis (EDA)
You can run the interactive EDA script using an IDE that supports `# %%` notebook cells (like VSCode) or via Jupyter Notebook.
```bash
jupyter notebook notebooks/01_EDA_and_Preprocessing.py
```

### Phase 3: Train the Model
Run the machine learning pipeline to preprocess data, train the XGBoost model, and save the artifact.
```bash
python src/train.py
```
*Output: Prints Accuracy, Classification Report, and saves `models/model.joblib`.*

### Phase 4: Start the FastAPI Scoring Service
Launch the API to serve the trained model.
```bash
uvicorn main:app --reload
```
*Output: Server starts at `http://127.0.0.1:8000`*

### Phase 5: Test the Prediction API
You can test the API by navigating to the interactive Swagger UI documentation at:
**http://127.0.0.1:8000/docs**

Or, you can use `curl` to send a POST request:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Age": 35,
  "Gender": "Female",
  "TenureMonths": 5,
  "ContractType": "Month-to-month",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 95.5,
  "TotalCharges": 477.5,
  "SupportCalls": 4
}'
```
*Expected Output: High churn probability based on short tenure, month-to-month contract, and high support calls.*

---

## 8. Interview Preparation Notes
If you are presenting this project in an interview:
- **Data Imbalance:** Be prepared to discuss how you handled imbalanced classes (you can mention `scale_pos_weight` in XGBoost or SMOTE as next steps).
- **Why XGBoost:** Explain that XGBoost handles non-linear relationships well, requires less preprocessing for numerical features than deep learning, and is the industry standard for tabular data.
- **FastAPI:** Highlight that FastAPI is modern, fast (built on Starlette), and automatically generates Swagger documentation, which is crucial for collaborating with Frontend/Next.js developers.
