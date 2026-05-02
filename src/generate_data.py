import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)

def generate_customer_data(num_records=5000):
    data = []
    for _ in range(num_records):
        # Demographics
        customer_id = fake.uuid4()
        age = np.random.randint(18, 70)
        gender = np.random.choice(["Male", "Female"])
        
        # Account Info
        tenure_months = np.random.randint(1, 72)
        contract_type = np.random.choice(["Month-to-month", "One year", "Two year"], p=[0.5, 0.3, 0.2])
        payment_method = np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
        
        # Usage Metrics
        monthly_charges = round(np.random.uniform(20.0, 120.0), 2)
        total_charges = round(monthly_charges * tenure_months + np.random.normal(0, 50), 2)
        total_charges = max(0, total_charges) # Ensure no negative total charges
        
        # Support & Satisfaction
        support_calls = np.random.randint(0, 10)
        
        # Synthesizing Churn logic (Virtual Simulation)
        # Higher probability to churn if: Month-to-month contract, high support calls, low tenure
        churn_prob = 0.1
        if contract_type == "Month-to-month": churn_prob += 0.3
        if support_calls > 3: churn_prob += 0.2
        if tenure_months < 12: churn_prob += 0.2
        if monthly_charges > 80: churn_prob += 0.1
        
        churn_prob = min(0.95, churn_prob) # Cap probability
        churn = np.random.choice(["Yes", "No"], p=[churn_prob, 1 - churn_prob])
        
        data.append([
            customer_id, age, gender, tenure_months, contract_type, 
            payment_method, monthly_charges, total_charges, support_calls, churn
        ])
        
    df = pd.DataFrame(data, columns=[
        "CustomerID", "Age", "Gender", "TenureMonths", "ContractType", 
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "SupportCalls", "Churn"
    ])
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/customer_churn_data.csv", index=False)
    print(f"Successfully generated {num_records} records in data/customer_churn_data.csv")

if __name__ == "__main__":
    generate_customer_data()
