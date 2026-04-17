import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

# ---------------------------
# 1. LOAD DATA
# ---------------------------
df = pd.read_csv("FutureEngineering.csv")

# ---------------------------
# 2. HANDLE MISSING VALUES
# ---------------------------
df["income"] = df["income"].fillna(df["income"].median())
df["age"] = df["age"].fillna(df["age"].median())
df["credit_score"] = df["credit_score"].fillna(df["credit_score"].median())
df["account_balance"] = df["account_balance"].fillna(df["account_balance"].median())
df["employment_type"] = df["employment_type"].fillna(df["employment_type"].mode()[0])

# ---------------------------
# 3. REMOVE OUTLIERS
# ---------------------------
df = df[df["income"] < df["income"].quantile(0.99)]

# ---------------------------
# 4. FEATURE ENGINEERING
# ---------------------------
df["debt_ratio"] = df["loan_amount"] / (df["income"] + 1)
df["risk_score"] = df["late_payments"] * 2 + (1 - df["credit_score"] / 850)
df["stability"] = df["years_employed"] / (df["age"] + 1)

# ---------------------------
# 5. DROP UNUSED COLUMNS
# ---------------------------
df.drop("customer_id", axis=1, inplace=True)

# ---------------------------
# 6. ENCODING
# ---------------------------
df = pd.get_dummies(df, columns=[
    "gender",
    "city",
    "education",
    "marital_status",
    "employment_type"
])

# ---------------------------
# 7. SPLIT DATA
# ---------------------------
X = df.drop("default", axis=1)
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# 8. SCALING
# ---------------------------
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# ---------------------------
# 9. CROSS VALIDATION
# ---------------------------
cv_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_score = cross_val_score(cv_model, X_train, y_train, cv=cv)

print("Cross Validation Scores:", cv_score)
print("Average CV Score:", cv_score.mean())

# ---------------------------
# 10. TRAIN FINAL MODEL
# ---------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------
# 11. EVALUATION
# ---------------------------
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_proba))

# ---------------------------
# 12. SAVE MODEL FILES
# ---------------------------
os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(X.columns.tolist(), "model/columns.pkl")

print("\n Model, scaler, and columns saved successfully!")