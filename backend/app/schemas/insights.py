from pydantic import BaseModel,Field
from typing import List

class TransactionItem(BaseModel):
    Time:float
    Amount:float
    V1:float
    V2:float
    V3:float
    V4:float
    V5:float
    V6:float
    V7:float
    V8:float
    V9:float
    V10:float
    V11:float
    V12:float
    V13:float
    V14:float
    V15:float
    V16:float
    V17:float
    V18:float
    V19:float
    V20:float
    V21:float
    V22:float
    V23:float
    V24:float
    V25:float
    V26:float
    V27:float
    V28:float

class InsightsRequest(BaseModel):
    transactions:List[TransactionItem]=Field(
        ..., min_length=1,max_length=10_000
    )
class TransactionResult(BaseModel):
    index : int
    amount :float
    fraud_probability : float
    is_fraud : bool
    risk_level : str

class RiskBreakdown(BaseModel):
    low : int
    medium : int
    high : int
class InsightsResponse(BaseModel):
    total_transactions : int
    flagged_count: int
    risk_breakdown : RiskBreakdown
    fraud_rate_pct: float
    total_amount: float
    avg_amount: float
    avg_fraud_prob: float
    highest_risk:List[TransactionResult]
    results: List[TransactionResult]