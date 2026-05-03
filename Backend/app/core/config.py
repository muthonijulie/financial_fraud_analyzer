from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent.parent
class Settings(BaseSettings):
    APP_Name:str="Financial Analyzer"
    VERSION:str="0.1.0"
    DEBUG:bool=False

    MODEL_PATH : Path = BASE_DIR / "artifacts" / "fraud_model.pkl"
    SCALER_PATH: Path =BASE_DIR / "artifacts" / "scaler.pkl"
    CONFIG_PATH: Path = BASE_DIR / "artifacts" / "model_config.json"  
    model_config = SettingsConfigDict(env_file=".env")
settings=Settings()