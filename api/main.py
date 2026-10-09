
from database.database import create_table, save_transaction, get_transactions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI(title="TrustLedger API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://trust-ledger.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()

model = joblib.load("ml/fraud_model.pkl")

dataset = pd.read_csv("data/sample_transactions.csv")

normal_count = 284315
fraud_count = 492

tn = 56856
fp = 8
fn = 21
tp = 77

model_metrics = {
    "accuracy": 99.95,
    "precision": 90.59,
    "recall": 78.57,
    "f1_score": 84.15,
    "roc_auc": 95.73
}


@app.get("/")
def home():
    return {
        "message": "TrustLedger API is running!"
    }


@app.post("/predict")
def predict(transaction: dict):
    data = pd.DataFrame([transaction])

    probability = model.predict_proba(data)[0][1]

    trust_score = round((1 - probability) * 100, 2)

    if trust_score >= 80:
        risk = "LOW"
    elif trust_score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    fraud_probability = round(probability * 100, 2)

    save_transaction(
        transaction["Amount"],
        fraud_probability,
        trust_score,
        risk
    )

    return {
        "fraud_probability": fraud_probability,
        "trust_score": trust_score,
        "risk_level": risk
    }


@app.get("/transactions")
def transactions():
    rows = get_transactions()

    return [
        {
            "id": row[0],
            "amount": row[1],
            "fraud_probability": row[2],
            "trust_score": row[3],
            "risk_level": row[4]
        }
        for row in rows
    ]


@app.get("/stats")
def stats():
    rows = get_transactions()

    total = len(rows)
    low = sum(1 for row in rows if row[4] == "LOW")
    medium = sum(1 for row in rows if row[4] == "MEDIUM")
    high = sum(1 for row in rows if row[4] == "HIGH")

    return {
        "total": total,
        "low": low,
        "medium": medium,
        "high": high
    }


@app.get("/sample-transactions")
def sample_transactions():
    samples = dataset.sample(10, random_state=42)
    return samples.to_dict(orient="records")


@app.get("/model-performance")
def model_performance():
    return model_metrics


@app.get("/analytics")
def analytics():
    return {
        "normal_count": normal_count,
        "fraud_count": fraud_count,
        "confusion_matrix": {
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp
        }
    }


@app.get("/model-comparison")
def model_comparison():
    return {
        "models": {
            "Logistic Regression": {
                "accuracy": 97.28,
                "precision": 5.52,
                "recall": 91.84,
                "f1_score": 10.42,
                "roc_auc": 97.21
            },
            "Random Forest": {
                "accuracy": 99.95,
                "precision": 90.59,
                "recall": 78.57,
                "f1_score": 84.15,
                "roc_auc": 95.73
            }
        },
        "selected_model": "Random Forest"
    }


@app.get("/feature-importance")
def feature_importance():
    feature_names = [
        "Time",
        "V1", "V2", "V3", "V4", "V5", "V6", "V7",
        "V8", "V9", "V10", "V11", "V12", "V13", "V14",
        "V15", "V16", "V17", "V18", "V19", "V20", "V21",
        "V22", "V23", "V24", "V25", "V26", "V27", "V28",
        "Amount"
    ]

    importances = model.feature_importances_

    features = []

    for name, importance in zip(feature_names, importances):
        features.append({
            "feature": name,
            "importance": round(float(importance) * 100, 2)
        })

    features.sort(
        key=lambda x: x["importance"],
        reverse=True
    )

    return {
        "features": features[:10]
    }
