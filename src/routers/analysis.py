"""
Router para endpoints de análise de código.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.logs import logger
from agents.supervisor import analyze_code_with_supervisor
from utils.structured_formatter import StructuredFormatter


class AnalyzeRequest(BaseModel):
    """Schema para requisição de análise de código."""

    python_code: str
    file_path: str | None = None
    output_format: str = "default"  # "default" ou "structured"
    project_name: str = "Code"  # Nome do projeto para formato estruturado


class AnalyzeResponse(BaseModel):
    """Schema para resposta de análise de código."""

    total_smells_detected: int
    code_smells: list[dict]
    agents_executed: int
    output_format: str = "default"


router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analisa código Python para detectar code smells usando múltiplos agentes especializados.

    Args:
        request: Requisição contendo o código Python a ser analisado

    Returns:
        AnalyzeResponse com os code smells detectados

    Raises:
        HTTPException: Se houver erro na análise
    """
    try:
        logger.info("Iniciando análise de código")

        if not request.python_code or not request.python_code.strip():
            raise HTTPException(
                status_code=400, detail="O código Python não pode estar vazio"
            )

        result = await analyze_code_with_supervisor(request.python_code)

        code_smells = result["code_smells"]

        # Se formato estruturado for solicitado, converte os resultados
        if request.output_format.lower() == "structured":
            formatter = StructuredFormatter(
                code=request.python_code,
                file_path=request.file_path or "unknown.py"
            )
            code_smells = formatter.format_results(
                code_smells=code_smells,
                project_name=request.project_name
            )

        logger.info(
            f"Análise concluída: {result['total_smells_detected']} code smells detectados"
        )

        return AnalyzeResponse(
            total_smells_detected=result["total_smells_detected"],
            code_smells=code_smells,
            agents_executed=result["agents_executed"],
            output_format=request.output_format,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao analisar código: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao analisar código: {str(e)}"
        )
