
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database.database import (
    create_table,
    save_transaction,
    get_transactions,
)

app = FastAPI(title="TrustLedger API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://trust-ledger.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "ml" / "fraud_model.pkl"
DATASET_PATH = BASE_DIR / "data" / "sample_transactions.csv"

model = joblib.load(MODEL_PATH)
dataset = pd.read_csv(DATASET_PATH)

FEATURE_NAMES = list(model.feature_names_in_)

if len(FEATURE_NAMES) != 30:
    raise RuntimeError(
        f"Expected 30 model features, found {len(FEATURE_NAMES)}"
    )

create_table()

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
    "roc_auc": 95.73,
}


@app.get("/")
def home():
    return {"message": "TrustLedger API is running!"}


@app.post("/predict")
def predict(transaction: dict):
    missing = [
        name for name in FEATURE_NAMES
        if name not in transaction
    ]

    if missing:
        raise HTTPException(
            status_code=422,
            detail={"missing_features": missing},
        )

    try:
        values = [float(transaction[name]) for name in FEATURE_NAMES]
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=422,
            detail="All transaction features must be numeric.",
        )

    data = pd.DataFrame(
        [values],
        columns=FEATURE_NAMES,
    )

    try:
        probability = float(model.predict_proba(data)[0][1])
    except Exception as error:
        print(f"Model prediction failed: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"Model prediction failed: {type(error).__name__}: {error}",
        )

    fraud_probability = round(probability * 100, 2)
    trust_score = round((1 - probability) * 100, 2)

    if trust_score >= 80:
        risk = "LOW"
    elif trust_score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    try:
        save_transaction(
            float(transaction["Amount"]),
            fraud_probability,
            trust_score,
            risk,
        )
    except Exception as error:
        print(f"Saving transaction failed: {type(error).__name__}: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction completed, but saving failed: {error}",
        )

    return {
        "fraud_probability": fraud_probability,
        "trust_score": trust_score,
        "risk_level": risk,
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
            "risk_level": row[4],
        }
        for row in rows
    ]


@app.get("/stats")
def stats():
    rows = get_transactions()

    return {
        "total": len(rows),
        "low": sum(1 for row in rows if row[4] == "LOW"),
        "medium": sum(1 for row in rows if row[4] == "MEDIUM"),
        "high": sum(1 for row in rows if row[4] == "HIGH"),
    }


@app.get("/sample-transactions")
def sample_transactions():
    samples = dataset.sample(
        n=min(10, len(dataset)),
        random_state=42,
    )
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
            "true_positive": tp,
        },
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
                "roc_auc": 97.21,
            },
            "Random Forest": model_metrics,
        },
        "selected_model": "Random Forest",
    }


@app.get("/feature-importance")
def feature_importance():
    if not hasattr(model, "feature_importances_"):
        raise HTTPException(
            status_code=500,
            detail="The loaded model does not provide feature importance.",
        )

    features = [
        {
            "feature": name,
            "importance": round(float(importance) * 100, 2),
        }
        for name, importance in zip(
            FEATURE_NAMES,
            model.feature_importances_,
        )
    ]

    features.sort(
        key=lambda item: item["importance"],
        reverse=True,
    )

    return {"features": features[:10]}
