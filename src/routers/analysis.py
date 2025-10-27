"""
Router para endpoints de análise de código.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.logs import logger
from supervisor import analyze_code_with_supervisor


class AnalyzeRequest(BaseModel):
    """Schema para requisição de análise de código."""

    python_code: str
    file_path: str | None = None


class AnalyzeResponse(BaseModel):
    """Schema para resposta de análise de código."""

    total_smells_detected: int
    code_smells: list[dict]
    agents_executed: int


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
        logger.info(
            f"Iniciando análise de código"
            + (f" do arquivo {request.file_path}" if request.file_path else "")
        )

        # Valida que o código não está vazio
        if not request.python_code or not request.python_code.strip():
            raise HTTPException(
                status_code=400, detail="O código Python não pode estar vazio"
            )

        # Executa a análise usando o supervisor
        result = await analyze_code_with_supervisor(request.python_code)

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
        raise HTTPException(status_code=500, detail=f"Erro ao analisar código: {str(e)}")
