# TrustLedger

## AI-Powered Financial Fraud Detection & Risk Assessment Platform

TrustLedger is a full-stack machine learning application that analyzes financial transactions, predicts fraud probability, generates a trust/risk score, and provides an interactive dashboard for transaction monitoring and model analysis.

The system combines a Random Forest fraud detection model with a FastAPI backend, React frontend, and SQLite database.

---

## Features

- AI-powered credit card fraud detection
- Fraud probability prediction
- Transaction trust/risk scoring
- Low, Medium, and High risk classification
- Random Forest fraud detection model
- Logistic Regression vs Random Forest comparison
- Model performance evaluation
- Feature importance analysis
- Confusion matrix visualization
- Fraud vs normal transaction analytics
- Risk distribution dashboard
- Transaction history
- SQLite database storage
- REST API using FastAPI
- Interactive React dashboard

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │    React Frontend   │
                    │      Dashboard      │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │   Prediction Layer  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Random Forest   │          │ SQLite Database │
       │ Fraud Model     │          │ Transaction Log │
       └─────────────────┘          └─────────────────┘
                │
                ▼
       ┌─────────────────┐
       │ Fraud Probability│
       │ Trust Score      │
       │ Risk Level       │
       └─────────────────┘