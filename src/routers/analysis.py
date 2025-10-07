import traceback
from typing import Any

from agents.workflow import create_supervisor
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_anthropic import ChatAnthropic

from agents.complexity_agent import create_complexity_agent
from agents.structure_agent import create_structure_agent
from config.logs import logger
from config.settings import settings
from schemas.requests import AnalyzeCodeRequest
from tools.analyze_class_structure import analyze_class_structure
from tools.analyze_cyclomatic_complexity import analyze_cyclomatic_complexity
from tools.detect_feature_envy import detect_feature_envy

router = APIRouter(prefix="/api/v1", tags=["analysis"])


def create_workflow() -> Any:
    """
    Cria o workflow completo com todos os agentes e ferramentas.

    Returns:
        Any: Workflow compilado pronto para execução
    """
    try:
        llm = ChatAnthropic(
            model_name=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )
        logger.info("LLM criado com sucesso")

        complexity_tools = [analyze_cyclomatic_complexity]
        structure_tools = [analyze_class_structure, detect_feature_envy]
        logger.info(
            f"Ferramentas carregadas: {len(complexity_tools)} complexidade, {len(structure_tools)} estrutura"
        )

        complexity_agent = create_complexity_agent(llm, complexity_tools)
        logger.info("Agente de complexidade criado")

        structure_agent = create_structure_agent(llm, structure_tools)
        logger.info("Agente de estrutura criado")

        workflow = create_supervisor(llm, complexity_agent, structure_agent)
        logger.info("Workflow supervisor criado com sucesso")

        return workflow
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"Mensagem: {str(e)}")
        logger.error("Traceback completo:")
        logger.error(traceback.format_exc())
        raise


@router.post("/analyze")
async def analyze_code(request: AnalyzeCodeRequest):
    """
    Analisa código Python em busca de code smells usando streaming.

    Args:
        request (AnalyzeCodeRequest): Requisição contendo o código a ser analisado

    Returns:
        StreamingResponse: Stream de eventos do workflow

    Raises:
        HTTPException: Se ocorrer um erro durante a análise
    """
    try:
        file_info = f" - Arquivo: {request.file_name}" if request.file_name else ""
        logger.info(f"Iniciando análise de código{file_info}")

        workflow = create_workflow()

        initial_state = {
            "messages": [],
            "python_code": request.code,
            "file": request.file_name,
            "code_smells": [],
            "next": "",
            "finished_agents": [],
        }

        async def event_stream():
            """
            Gera eventos do workflow em tempo real.

            Yields:
                str: Texto com os eventos do workflow
            """
            try:
                yield "=== Iniciando análise de code smells ===\n\n"

                async for event in workflow.astream(initial_state):
                    if event:
                        node_name = list(event.keys())[0]
                        yield f"[{node_name}] Processando...\n"

                        node_data = event.get(node_name, {})
                        messages = node_data.get("messages", [])

                        if messages:
                            last_message = (
                                messages[-1] if isinstance(messages, list) else messages
                            )
                            if hasattr(last_message, "content"):
                                yield f"{last_message.content}\n\n"

                yield "\n=== Análise concluída com sucesso ===\n"

            except Exception as e:
                error_msg = f"Mensagem: {str(e)}\n\n{traceback.format_exc()}"
                logger.error(error_msg)
                yield error_msg

        return StreamingResponse(
            event_stream(),
            media_type="text/plain",
        )

    except Exception as e:
        error_details = (
            f"Erro ao processar requisição\n"
            f"Mensagem: {str(e)}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
        logger.error(error_details)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Verifica o status da API.

    Returns:
        dict: Status da API
    """
    return {"status": "Ok", "message": "API is running"}
