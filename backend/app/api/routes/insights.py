from fastapi import APIRouter, HTTPException
from app.schemas.insights import InsightsRequest, InsightsResponse
from app.ml.model import fraud_model
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/insights",
    response_model=InsightsResponse,
    summary="Analyze a batch of transactions",
    tags=["Insights"]
)
async def get_insights(payload: InsightsRequest) -> InsightsResponse:
  
    try:
        data   = [t.model_dump() for t in payload.transactions]
        result = fraud_model.analyze(data)
        logger.info(
            f"Batch analyzed — {result['total_transactions']} transactions | "
            f"{result['flagged_count']} flagged"
        )
        return InsightsResponse(**result)
    except Exception as e:
        logger.error(f"Insights error: {e}")
        raise HTTPException(status_code=500, detail=str(e))