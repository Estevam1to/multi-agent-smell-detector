"""Router para endpoints de análise de código."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.logs import logger
from agents.supervisor import analyze_code_with_supervisor, analyze_code_with_supervisor_v2


class AnalyzeRequest(BaseModel):
    python_code: str
    file_path: str | None = None
    output_format: str = "default"
    project_name: str = "Code"
    use_structured_output: bool = False


class AnalyzeResponse(BaseModel):
    total_smells_detected: int
    code_smells: list[dict]
    agents_executed: int
    output_format: str = "default"


router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest) -> AnalyzeResponse:

    try:
        logger.info("Iniciando análise de código")

        if not request.python_code or not request.python_code.strip():
            raise HTTPException(
                status_code=400, detail="O código Python não pode estar vazio"
            )

        if request.use_structured_output:
            result = await analyze_code_with_supervisor_v2(
                request.python_code,
                request.file_path or "unknown.py",
                request.project_name
            )
        else:
            result = await analyze_code_with_supervisor(request.python_code)

        logger.info(
            f"Análise concluída: {result['total_smells_detected']} code smells detectados"
        )

        return AnalyzeResponse(
            total_smells_detected=result["total_smells_detected"],
            code_smells=result["code_smells"],
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
