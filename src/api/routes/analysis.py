"""Endpoints de análise de código."""

from fastapi import APIRouter, HTTPException

from config.logs import logger
from core.supervisor import analyze_code
from api.models import AnalyzeRequest, AnalyzeResponse

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analisa código Python e retorna code smells."""
    try:
        if not request.python_code.strip():
            raise HTTPException(status_code=400, detail="Código vazio")

        result = await analyze_code(
            python_code=request.python_code,
            file_path=request.file_path or "unknown.py",
            project_name=request.project_name,
            parallel=True
        )

        logger.info(f"Análise concluída: {result['total_smells_detected']} smells")

        return AnalyzeResponse(
            total_smells_detected=result["total_smells_detected"],
            code_smells=result["code_smells"],
            agents_executed=result["agents_executed"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
