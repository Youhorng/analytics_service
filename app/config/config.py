import os
from pydantic_settings import BaseSettings # type: ignore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Server settings
    PORT: int = int(os.getenv("PORT", 8005))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # MongoDB settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/analytics")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "fraud_detection")
    
    model_config = {
        "env_file": ".env"
    }

# Create settings instance
settings = Settings()