"""Router para endpoints de análise de código."""

from fastapi import APIRouter, HTTPException

from config.logs import logger
from core.agents.supervisor.supervisor import analyze_code_with_supervisor_v2
from api.models import AnalyzeRequest, AnalyzeResponse


router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest) -> AnalyzeResponse:

    try:
        logger.info("Iniciando análise de código")

        if not request.python_code or not request.python_code.strip():
            raise HTTPException(
                status_code=400, detail="O código Python não pode estar vazio"
            )

        result = await analyze_code_with_supervisor_v2(
            request.python_code,
            request.file_path or "unknown.py",
            request.project_name
        )

        logger.info(
            f"Análise concluída: {result['total_smells_detected']} code smells detectados"
        )

        return AnalyzeResponse(
            total_smells_detected=result["total_smells_detected"],
            code_smells=result["code_smells"],
            agents_executed=result["agents_executed"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao analisar código: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao analisar código: {str(e)}"
        )
