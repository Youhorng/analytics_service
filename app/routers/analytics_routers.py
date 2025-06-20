from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from app.services.analytics_services import analytics_service
from app.db.database import get_db

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
    try:
        db = get_db()
        result = await analytics_service.get_fraud_summary(db)
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.get("/categories", summary="Get fraud by category")
async def get_fraud_by_category():
    """
    Get fraud statistics grouped by merchant category:
    - Number of frauds per category
    - Percentage of total fraud
    - Average fraud amount per category
    """
    try:
        db = get_db()
        result = await analytics_service.get_fraud_by_category(db)
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")