import os
import joblib
import pandas as pd
import logging
from fastapi import HTTPException

# basic logging
logging.basicConfig(level=logging.INFO)

# load model files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model", "model.pkl")
scaler_path = os.path.join(BASE_DIR, "model", "scaler.pkl")
columns_path = os.path.join(BASE_DIR, "model", "columns.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
columns = joblib.load(columns_path)


def predict(data: dict):
    try:
        logging.info("Incoming request")

        # convert input to dataframe
        df = pd.DataFrame([data])

        # ---- feature engineering ----
        df["debt_ratio"] = df["loan_amount"] / (df["income"] + 1)
        df["risk_score"] = df["late_payments"] * 2 + (1 - df["credit_score"] / 850)
        df["stability"] = df["years_employed"] / (df["age"] + 1)

        # ---- encoding ----
        df = pd.get_dummies(df)

        # ---- align columns ----
        df = df.reindex(columns=columns, fill_value=0)

        # ---- scaling ----
        df_scaled = scaler.transform(df)

        # ---- prediction ----
        pred = model.predict(df_scaled)[0]
        prob = model.predict_proba(df_scaled)[0][1]

        # ---- response ----
        result = {
            "risk_level": "HIGH" if pred == 1 else "LOW",
            "confidence": f"{round(prob * 100, 2)}%",
            "probability": round(float(prob), 3),
            "message": "Customer may default" if pred == 1 else "Customer is safe"
        }

        return result

    except KeyError as err:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {err}"
        )

    except Exception as err:
        logging.error(f"Prediction failed: {err}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong during prediction"
        )