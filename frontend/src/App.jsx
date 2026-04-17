import { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [form, setForm] = useState({
    income: "",
    age: "",
    gender: "male",
    credit_score: "",
    loan_amount: "",
    interest_rate: "",
    years_employed: "",
    existing_loans: "",
    late_payments: "",
    account_balance: "",
    city: "",
    education: "",
    marital_status: "",
    employment_type: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const toNumber = (val) => {
    const num = Number(val);
    return isNaN(num) ? 0 : num;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const payload = {
      income: toNumber(form.income),
      age: toNumber(form.age),
      gender: form.gender || "male",
      credit_score: toNumber(form.credit_score),
      loan_amount: toNumber(form.loan_amount),
      interest_rate: toNumber(form.interest_rate),
      years_employed: toNumber(form.years_employed),
      existing_loans: toNumber(form.existing_loans),
      late_payments: toNumber(form.late_payments),
      account_balance: toNumber(form.account_balance),
      city: form.city || "unknown",
      education: form.education || "unknown",
      marital_status: form.marital_status || "unknown",
      employment_type: form.employment_type || "unknown",
    };

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", payload);

      setResult(res.data); // 🔥 store full object
    } catch (err) {
      console.log(err);
      setResult({ error: "API ERROR" });
    }

    setLoading(false);
  };

  const getRiskColor = (level) => {
    if (level === "LOW") return "low";
    if (level === "MEDIUM") return "medium";
    if (level === "HIGH") return "high";
    return "unknown";
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1 className="title">AI Loan Risk Predictor</h1>
        <p className="subtitle">Smart financial intelligence powered by ML</p>

        <form className="form-grid" onSubmit={handleSubmit}>
          <input name="income" placeholder="Income" onChange={handleChange} />
          <input name="age" placeholder="Age" onChange={handleChange} />

          <select name="gender" onChange={handleChange}>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>

          <input name="credit_score" placeholder="Credit Score" onChange={handleChange} />
          <input name="loan_amount" placeholder="Loan Amount" onChange={handleChange} />
          <input name="interest_rate" placeholder="Interest Rate" onChange={handleChange} />
          <input name="years_employed" placeholder="Years Employed" onChange={handleChange} />
          <input name="existing_loans" placeholder="Existing Loans" onChange={handleChange} />
          <input name="late_payments" placeholder="Late Payments" onChange={handleChange} />
          <input name="account_balance" placeholder="Account Balance" onChange={handleChange} />

          <input name="city" placeholder="City" onChange={handleChange} />
          <input name="education" placeholder="Education" onChange={handleChange} />
          <input name="marital_status" placeholder="Marital Status" onChange={handleChange} />
          <input name="employment_type" placeholder="Employment Type" onChange={handleChange} />

          <button className="predict-btn" type="submit" disabled={loading}>
            {loading ? "AI Analyzing..." : "Predict Risk"}
          </button>
        </form>

        {/* 🔥 RESULT CARD */}
        {result && !result.error && (
          <div className={`result-card ${getRiskColor(result.risk_level)}`}>
            <h2>{result.risk_level} RISK</h2>

            <p className="confidence">
              Confidence: {result.confidence}
            </p>

            <div className="bar">
              <div
                className="fill"
                style={{ width: `${result.probability * 100}%` }}
              ></div>
            </div>

            <p className="message">{result.message}</p>
          </div>
        )}

        {result?.error && (
          <div className="error-box">{result.error}</div>
        )}
      </div>
    </div>
  );
}