import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from app.core.config import settings
import logging
logger = logging.getLogger(__name__)
class FraudDetectionModel:
    def __init__(self):
        self.model=None
        self._scaler=None
        self._config=None
        self._threshold=None
        self._input_features=None

    def load(self):
        logger.info("Logging fraud detection model and scaler")
        self._model=joblib.load(settings.MODEL_PATH)
        self._scaler=joblib.load(settings.SCALER_PATH)
        with open(settings.CONFIG_PATH) as f:
            self._config=json.load(f)
        self._threshold=self._config.get("threshold")
        self._input_features=self._config.get("input_features")

        logger.info(f"Model loaded :{self._threshold}")
        logger.info(f"Model loaded :{len(self._input_features)}")

    def get_risk_level(self,probability:float)->str:
        if probability<0.3:
            return "LOW"
        elif probability<0.7:
            return "MEDIUM"
        return "HIGH"
    
    def predict(self,data:dict)->dict:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load() before prediction.")
        df=pd.DataFrame([data])[self._input_features]#build dataframe in exact column it was trained on
        df[['Amount','Time']]=self._scaler.transform(df[['Amount','Time']])#scale the data
        fraud_prob=float(self._model.predict_proba(df)[0][1])
        is_fraud=fraud_prob>=self._threshold

        return{
            "is_fraud":is_fraud,
            "probability":round(fraud_prob,4),
            "risk":self.get_risk_level(fraud_prob),
            "threshold":self._threshold,
            "message":("The transaction is likely to be fraudulent" 
                if is_fraud else 
                "The transaction is unlikely to be fraudulent"
        )
        }
    
fraud_model=FraudDetectionModel()#module level singleton

