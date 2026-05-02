# %% [markdown]
# # Customer Churn Data: Exploratory Data Analysis
# This notebook demonstrates how to load, visualize, and analyze the customer churn dataset.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic parameters
sns.set_theme(style="whitegrid")

# %%
# Load the dataset
# Adjust path assuming the script is run from notebooks/ or root
try:
    df = pd.read_csv('../data/customer_churn_data.csv')
except FileNotFoundError:
    df = pd.read_csv('data/customer_churn_data.csv')

df.head()

# %%
# Basic Information
df.info()

# %%
# Summary Statistics
df.describe()

# %%
# Class distribution (Churn vs No Churn)
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Churn', palette='Set2')
plt.title('Churn Distribution')
plt.show()

# %% [markdown]
# ## Feature Analysis

# %%
# Numerical Features against Churn
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.boxplot(ax=axes[0], data=df, x='Churn', y='TenureMonths', palette='Set2')
axes[0].set_title('Tenure vs Churn')

sns.boxplot(ax=axes[1], data=df, x='Churn', y='MonthlyCharges', palette='Set2')
axes[1].set_title('Monthly Charges vs Churn')

sns.boxplot(ax=axes[2], data=df, x='Churn', y='SupportCalls', palette='Set2')
axes[2].set_title('Support Calls vs Churn')

plt.tight_layout()
plt.show()

# %%
# Categorical Features against Churn
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.countplot(ax=axes[0], data=df, x='ContractType', hue='Churn', palette='Set2')
axes[0].set_title('Contract Type vs Churn')

sns.countplot(ax=axes[1], data=df, x='PaymentMethod', hue='Churn', palette='Set2')
axes[1].set_title('Payment Method vs Churn')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Correlation Analysis

# %%
# Encoding target for correlation map
df_corr = df.copy()
df_corr['Churn'] = df_corr['Churn'].map({'Yes': 1, 'No': 0})
numerical_cols = ['Age', 'TenureMonths', 'MonthlyCharges', 'TotalCharges', 'SupportCalls', 'Churn']

plt.figure(figsize=(8, 6))
sns.heatmap(df_corr[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

# %% [markdown]
# ### Observations:
# - Customers with Month-to-month contracts are more likely to churn.
# - Higher number of support calls is strongly correlated with churn.
# - Longer tenure indicates a lower likelihood of churning.
