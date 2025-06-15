from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from app.db.database import connect_to_mongodb, close_mongodb_connection
from app.routers import analytics_routers
from app.config.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI application
app = FastAPI(
    title="Fraud Analytics Service",
    description="Simple analytics for fraud detection system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(analytics_routers.router)

@app.on_event("startup")
async def startup_event():
    """Connect to database when app starts"""
    logging.info("Starting Analytics Service")
    try:
        await connect_to_mongodb()
        logging.info("MongoDB connection established")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection when app shuts down"""
    await close_mongodb_connection()
    logging.info("Analytics Service shutdown")

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Fraud Analytics Service",
        "version": "1.0.0",
        "endpoints": {
            "/analytics/summary": "Overview of fraud statistics",
            "/analytics/categories": "Fraud distribution by category"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)