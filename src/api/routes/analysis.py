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

        logger.info("Análise concluída: %s smells", result["total_smells_detected"])

        return AnalyzeResponse(
            total_smells_detected=result["total_smells_detected"],
            code_smells=result["code_smells"],
            agents_executed=result["agents_executed"],
        )

    except HTTPException:
        raise
    except (ValueError, KeyError, AttributeError) as e:
        logger.error("Erro de validação: %s", e, exc_info=True)
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(e)}")
    except Exception as e:  # pylint: disable=broad-except
        # Catch-all necessário para erros inesperados do supervisor/LLM
        logger.error("Erro inesperado: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
