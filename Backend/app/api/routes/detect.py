from fastapi import APIRouter,HTTPException
from app.schemas.transaction import TransactionRequest,TransactionResponse
from app.ml.model import fraud_model
import logging

logger=logging.getLogger(__name__)
router=APIRouter()

@router.post("/predict",response_model=TransactionResponse)
async def detect_fraud(transaction:TransactionRequest)->TransactionResponse:
    try:
        result=fraud_model.predict(transaction.model_dump())
        logger.info(
            f"Prediction-fraud:{result['is_fraud']}|"
            f"prob:{result['fraud_probability']:.4f}"
        )
        return TransactionResponse(**result)
    except Exception as e:
        logger.error(f"Pred errror:{e}")
        raise HTTPException(status_code=500,detail=str(e))
        