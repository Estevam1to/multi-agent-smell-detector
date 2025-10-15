import traceback
import json

from fastapi import APIRouter, HTTPException
from langchain_anthropic import ChatAnthropic

from agents import long_method_agent_analyze, long_parameter_list_agent_analyze
from config.logs import logger
from config.settings import settings
from schemas.long_method_schemas import AnalyzeCodeRequest, AnalyzeCodeResponse, AgentResult, CodeSmellDetail

router = APIRouter(prefix="/api/v1", tags=["analysis"])


def parse_agent_response(analysis_text: str) -> list[CodeSmellDetail]:
    """
    Extrai code smells do texto de análise do agente.
    
    Args:
        analysis_text: Texto de resposta do agente
        
    Returns:
        Lista de CodeSmellDetail extraídos
    """
    code_smells = []
    
    try:
        # Tenta encontrar blocos JSON no texto
        import re
        json_pattern = r'```json\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, analysis_text, re.DOTALL)
        
        for match in matches:
            try:
                smell_data = json.loads(match)
                code_smell = CodeSmellDetail(**smell_data)
                code_smells.append(code_smell)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Erro ao fazer parse de JSON: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Erro ao extrair code smells: {e}")
    
    return code_smells


@router.post("/analyze", response_model=AnalyzeCodeResponse)
async def analyze_code(request: AnalyzeCodeRequest):
    """
    Analisa código Python em busca de code smells usando agentes especializados.
    
    Args:
        request: Requisição contendo o código a ser analisado
        
    Returns:
        Resposta com os code smells detectados
    """
    try:
        logger.info(f"Iniciando análise de código. Arquivo: {request.file_name}")
        
        results = []
        
        # Executa o Long Method Agent
        try:
            long_method_result = long_method_agent_analyze(
                code=request.code,
                file_name=request.file_name
            )
            
            if long_method_result["status"] == "sucesso":
                code_smells = parse_agent_response(long_method_result["analysis"])
                agent_result = AgentResult(
                    agent_name="LongMethodAgent",
                    status="sucesso",
                    code_smells=code_smells,
                    analysis_text=long_method_result["analysis"]
                )
            else:
                agent_result = AgentResult(
                    agent_name="LongMethodAgent",
                    status="erro",
                    code_smells=[],
                    error_message=long_method_result.get("mensagem", "Erro desconhecido")
                )
                
            results.append(agent_result)
            
        except Exception as e:
            logger.error(f"Erro no Long Method Agent: {e}")
            agent_result = AgentResult(
                agent_name="LongMethodAgent",
                status="erro",
                code_smells=[],
                error_message=str(e)
            )
            results.append(agent_result)
        
        # Executa o Long Parameter List Agent
        try:
            long_param_result = long_parameter_list_agent_analyze(
                code=request.code,
                file_name=request.file_name
            )
            
            if long_param_result["status"] == "sucesso":
                code_smells = parse_agent_response(long_param_result["analysis"])
                agent_result = AgentResult(
                    agent_name="LongParameterListAgent",
                    status="sucesso",
                    code_smells=code_smells,
                    analysis_text=long_param_result["analysis"]
                )
            else:
                agent_result = AgentResult(
                    agent_name="LongParameterListAgent",
                    status="erro",
                    code_smells=[],
                    error_message=long_param_result.get("mensagem", "Erro desconhecido")
                )
                
            results.append(agent_result)
            
        except Exception as e:
            logger.error(f"Erro no Long Parameter List Agent: {e}")
            agent_result = AgentResult(
                agent_name="LongParameterListAgent",
                status="erro",
                code_smells=[],
                error_message=str(e)
            )
            results.append(agent_result)
        
        # Calcula resumo consolidado
        total_smells = sum(len(result.code_smells) for result in results)
        agents_executados = len(results)
        agents_com_sucesso = len([r for r in results if r.status == "sucesso"])
        
        summary = {
            "total_code_smells": total_smells,
            "agents_executados": agents_executados,
            "agents_com_sucesso": agents_com_sucesso,
            "file_name": request.file_name,
            "severidades": {}
        }
        
        # Conta severidades
        for result in results:
            for smell in result.code_smells:
                severidade = smell.severity
                summary["severidades"][severidade] = summary["severidades"].get(severidade, 0) + 1
        
        response = AnalyzeCodeResponse(
            success=agents_com_sucesso > 0,
            message=f"Análise concluída. {total_smells} code smell(s) detectado(s) por {agents_com_sucesso}/{agents_executados} agente(s).",
            results=results,
            summary=summary
        )
        
        logger.info(f"Análise concluída com sucesso. Total de code smells: {total_smells}")
        return response
        
    except Exception as e:
        logger.error(f"Erro durante análise: {e}")
        logger.error(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno durante análise: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Verifica o status de saúde da API.
    
    Returns:
        Status de saúde dos componentes
    """
    try:
        # Testa conexão com Anthropic
        test_model = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY
        )
        
        # Teste simples
        test_response = test_model.invoke("Teste de conectividade")
        
        return {
            "status": "healthy",
            "components": {
                "api": "ok",
                "anthropic": "ok" if test_response else "error",
                "agents": {
                    "long_method_agent": "ok",
                    "long_parameter_list_agent": "ok"
                }
            },
            "timestamp": "2025-10-13"
        }
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-10-13"
        }
