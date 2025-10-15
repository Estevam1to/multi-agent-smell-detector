import traceback
import json

from fastapi import APIRouter, HTTPException

from config.logs import logger
from config.settings import settings

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze")
async def analyze_code() -> None:
    raise NotImplementedError("Endpoint /analyze is not implemented yet.")