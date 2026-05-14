from pydantic import BaseModel,Field,field_validator
from typing import Annotated

class TransactionRequest(BaseModel):
    Time:float=Field(...,description="Time of the transaction in seconds")
    Amount:float=Field(...,description="Amount of the transaction")
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

    @field_validator('Amount')
    @classmethod
    def amount_must_be_positive(cls,value):
        if value<0:
            raise ValueError("Amount must not be negative")
        return round(value,2)
    
class TransactionResponse(BaseModel):
    is_fraud:bool
    probability:float=Field(...,ge=0,le=1)
    risk:str
    threshold:float
    message:str

    model_config={"json_schema_extra":{
        "json":{
            "is_fraud":False,
            "probability":0.05,
            "risk":"Low",
            "threshold":0.5,
            "message":"The transaction is unlikely to be fraudulent"
        }
    }}