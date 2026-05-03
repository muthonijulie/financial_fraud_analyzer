from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import detect
from app.ml.model import fraud_model
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Starting the app")
    fraud_model.load()
    yield
    logger.info("Shut down")
app=FastAPI(
    title=settings.APP_Name,
    version=settings.VERSION,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(detect.router,prefix="/api/v1")

@app.get("/health",tags=["Health"])
async def health():
    return{"status":"ok","version":settings.VERSION}


