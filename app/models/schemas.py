from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class FraudSummary(BaseModel):
    """Response model for fraud summary statistics"""
    total_transactions: int = Field(..., description="Total number of transactions in the system")
    fraud_transactions: int = Field(..., description="Number of transactions flagged as fraud")
    fraud_percentage: float = Field(..., description="Percentage of transactions flagged as fraud")
    avg_fraud_probability: float = Field(..., description="Average fraud probability score")
    
class CategoryStat(BaseModel):
    """Statistics for a single category"""
    category: str = Field(..., description="Transaction category")
    count: int = Field(..., description="Number of fraudulent transactions")
    percentage: float = Field(..., description="Percentage of all fraud")
    avg_amount: float = Field(..., description="Average transaction amount")
    
class CategoryStats(BaseModel):
    """Response model for category-based fraud statistics"""
    total_fraud: int = Field(..., description="Total number of fraud transactions")
    categories: List[CategoryStat] = Field(..., description="Statistics by category")