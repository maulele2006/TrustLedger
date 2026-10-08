import pandas as pd
import joblib

# Load trained model
model = joblib.load("ml/fraud_model.pkl")


def predict_transaction(transaction):
    # Convert transaction into DataFrame
    data = pd.DataFrame([transaction])

    # Get fraud probability
    probability = model.predict_proba(data)[0][1]

    # Convert probability to Trust Score
    trust_score = round((1 - probability) * 100, 2)

    # Determine risk level
    if trust_score >= 80:
        risk = "LOW"
    elif trust_score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return trust_score, risk


# Test transaction
transaction = {
    "Time": 1000,
    "V1": 0,
    "V2": 0,
    "V3": 0,
    "V4": 0,
    "V5": 0,
    "V6": 0,
    "V7": 0,
    "V8": 0,
    "V9": 0,
    "V10": 0,
    "V11": 0,
    "V12": 0,
    "V13": 0,
    "V14": 0,
    "V15": 0,
    "V16": 0,
    "V17": 0,
    "V18": 0,
    "V19": 0,
    "V20": 0,
    "V21": 0,
    "V22": 0,
    "V23": 0,
    "V24": 0,
    "V25": 0,
    "V26": 0,
    "V27": 0,
    "V28": 0,
    "Amount": 100
}

score, risk = predict_transaction(transaction)

print("Trust Score:", score)
print("Risk Level:", risk)