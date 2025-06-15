from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.services.analytics_services import analytics_service
from app.db.database import db

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}}
)

@router.get("/summary", summary="Get fraud summary statistics")
async def get_fraud_summary():
    """
    Get summary statistics about fraud transactions:
    - Total transactions vs fraud transactions
    - Fraud percentage
    - Average fraud probability
    """
    result = await analytics_service.get_fraud_summary(db)
    
    if not result.get("success", False):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result

@router.get("/categories", summary="Get fraud by category")
async def get_fraud_by_category():
    """
    Get fraud statistics grouped by merchant category:
    - Number of frauds per category
    - Percentage of total fraud
    - Average fraud amount per category
    """
    result = await analytics_service.get_fraud_by_category(db)
    
    if not result.get("success", False):
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    
    return result