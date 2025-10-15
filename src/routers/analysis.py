import traceback
import json

from fastapi import APIRouter, HTTPException
from langchain_anthropic import ChatAnthropic

from agents import long_method_agent_analyze, long_parameter_list_agent_analyze
from config.logs import logger
from config.settings import settings
from schemas.long_method_schemas import AnalyzeCodeRequest, AnalyzeCodeResponse, AgentResult, CodeSmellDetail

router = APIRouter(prefix="/api/v1", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeCodeResponse)
async def analyze_code(request: AnalyzeCodeRequest) -> AnalyzeCodeResponse:
    raise NotImplementedError("Endpoint /analyze is not implemented yet.")