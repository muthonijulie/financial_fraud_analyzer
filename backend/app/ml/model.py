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
    def analyze(self,transactions:list[dict])->dict:
        if self._model is None:
            raise RuntimeError("Model not loaded.")
        
        df=pd.DataFrame(transactions)[self._input_features]
        df[['Amount','Time']]=self._scaler.transform(df[['Amount','Time']])
        probs=self._model.predict_proba(df)[:,1]
        amounts=pd.DataFrame(transactions)['Amount'].values
        results=[]
        for i,(prob,amount) in enumerate(zip(probs,amounts)):
            results.append({
                "index":i,
                "amount":round(float(amount),2),
                "fraud_probability":round(float(prob),4),
                "is_fraud":bool(prob>=self._threshold),
                "risk_level":self.get_risk_level(float(prob))
            })
        flagged=[r for r in results if r["is_fraud" ]]
        risk_counts={
            "low":sum(1 for r in results if r["risk_level"]=="LOW"),
            "medium":sum(1 for r in results if r["risk_level"]=="MEDIUM"),
            "high":sum(1 for r in results if r["risk_level"]=="HIGH")
        }
        top5=sorted(results,key=lambda x:x["fraud_probability"],reverse=True)[:5]
        return {
            "total_transactions":len(results),
            "flagged_count":len(flagged),
            "risk_breakdown":risk_counts,
            "fraud_rate_pct":round(100*len(flagged)/len(results),2),
            "total_amount":round(float(amounts.sum()),2),
            "avg_amount":round(float(amounts.mean()),2),
            "avg_fraud_prob":round(float(probs.mean()),6),
            "highest_risk":top5,
            "results":results
        }
fraud_model=FraudDetectionModel()

