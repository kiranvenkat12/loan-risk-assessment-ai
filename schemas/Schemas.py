from pydantic import BaseModel

class InputData(BaseModel):
    income: float
    age: int
    gender: str
    credit_score: int
    loan_amount: float
    interest_rate: float
    years_employed: int
    existing_loans: int
    late_payments: int
    account_balance: float
    city: str
    education: str
    marital_status: str
    employment_type: str