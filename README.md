# TrustLedger

### AI-Powered Financial Fraud Detection & Risk Analysis Platform

TrustLedger is a full-stack machine learning application that analyzes financial transactions, predicts the probability of fraud, and converts the prediction into an easy-to-understand risk assessment.

The platform combines a **Random Forest machine learning model**, **FastAPI backend**, **SQLite database**, and **React dashboard** into a complete end-to-end fraud detection system.

---
## 🖥️ Dashboard Preview

![TrustLedger Dashboard](docs/dashboard.png)
## 🚀 Key Features

- 🔍 **Fraud Detection** — Predict whether a transaction is potentially fraudulent
- 📊 **Fraud Probability** — Display the model's estimated probability of fraud
- 🛡️ **Risk Assessment** — Convert predictions into Low, Medium, and High risk levels
- 📈 **Model Performance** — View Accuracy, Precision, Recall, F1-Score, and ROC-AUC
- ⚖️ **Model Comparison** — Compare Random Forest with Logistic Regression
- 🔬 **Feature Importance** — Identify the features contributing most to predictions
- 📊 **Transaction Analytics** — View fraud/normal distribution and confusion matrix
- 🗄️ **Transaction History** — Store analyzed transactions using SQLite
- ⚡ **REST API** — FastAPI endpoints connecting the ML model with the frontend
- 💻 **Interactive Dashboard** — React-based interface for analyzing transactions

---

## 🖥️ Dashboard

TrustLedger provides an interactive dashboard for monitoring fraud detection performance and analyzing individual transactions.

The dashboard includes:

- Overall risk overview
- Model performance metrics
- Model comparison
- Feature importance
- Risk distribution
- Fraud vs. normal transaction analysis
- Confusion matrix
- Transaction analysis
- Transaction history

---

## 🧠 Machine Learning

TrustLedger uses a **Random Forest Classifier** trained on the Credit Card Fraud Detection dataset.

### Dataset

The dataset contains:

- **284,807 transactions**
- **492 fraudulent transactions**
- **30 input features**
- Severe class imbalance

The original dataset contains:

```text
Time
V1 - V28
Amount
Class