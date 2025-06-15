import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class AnalyticsService:
    """Simplified service for analyzing fraud transaction data"""
    
    async def get_fraud_summary(self, db) -> Dict[str, Any]:
        """
        Get summary statistics about fraud transactions
        
        Args:
            db: MongoDB database connection
            
        Returns:
            Dictionary with fraud summary statistics
        """
        try:
            # Get total transactions
            total_count = await db.transactions.count_documents({})
            
            # Get fraud transactions
            fraud_count = await db.transactions.count_documents({"is_fraud": True})
            
            # Calculate fraud percentage
            fraud_percentage = (fraud_count / total_count * 100) if total_count > 0 else 0
            
            # Get average fraud probability
            avg_probability = 0
            if fraud_count > 0:
                pipeline = [
                    {"$match": {"is_fraud": True}},
                    {"$group": {
                        "_id": None,
                        "avg_probability": {"$avg": "$fraud_probability"}
                    }}
                ]
                result = await db.transactions.aggregate(pipeline).to_list(1)
                avg_probability = result[0]["avg_probability"] if result else 0
            
            return {
                "success": True,
                "total_transactions": total_count,
                "fraud_transactions": fraud_count,
                "fraud_percentage": round(fraud_percentage, 2),
                "avg_fraud_probability": round(avg_probability, 4)
            }
        except Exception as e:
            logging.error(f"Error getting fraud summary: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
            
    async def get_fraud_by_category(self, db) -> Dict[str, Any]:
        """
        Get fraud statistics grouped by transaction category
        
        Args:
            db: MongoDB database connection
            
        Returns:
            Dictionary with category-based fraud statistics
        """
        try:
            # Get total fraud count
            total_fraud = await db.transactions.count_documents({"is_fraud": True})
            
            if total_fraud == 0:
                return {
                    "success": True,
                    "total_fraud": 0,
                    "categories": []
                }
            
            # Pipeline for aggregating fraud by category
            pipeline = [
                {
                    "$match": {"is_fraud": True}
                },
                {
                    "$group": {
                        "_id": {
                            "$ifNull": ["$category", 
                                       {"$ifNull": ["$merchant_category", "unknown"]}]
                        },
                        "count": {"$sum": 1},
                        "avg_amount": {"$avg": "$transaction_amount"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "category": {"$ifNull": ["$_id", "unknown"]},
                        "count": "$count",
                        "percentage": {"$round": [{"$multiply": [{"$divide": ["$count", total_fraud]}, 100]}, 2]},
                        "avg_amount": {"$round": ["$avg_amount", 2]}
                    }
                },
                {
                    "$sort": {"count": -1}
                }
            ]
            
            # Execute aggregation
            categories = await db.transactions.aggregate(pipeline).to_list(20)
            
            return {
                "success": True,
                "total_fraud": total_fraud,
                "categories": categories
            }
        except Exception as e:
            logging.error(f"Error getting fraud by category: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Create an instance of the service
analytics_service = AnalyticsService()