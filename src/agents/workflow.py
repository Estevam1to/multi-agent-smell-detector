import traceback
from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from config.logs import logger
from schemas.state import AgentState


def create_supervisor(
    llm: Any,
    complexity_agent: StateGraph,
    structure_agent: StateGraph,
) -> StateGraph:
    """
    Cria o agente supervisor que coordena os agentes especializados.

    Args:
        llm (Any): Instância do modelo de linguagem
        complexity_agent (StateGraph): Agente especializado em análise de complexidade
        structure_agent (StateGraph): Agente especializado em análise de estrutura

    Returns:
        StateGraph: Grafo de estados compilado com o supervisor e agentes
    """

    members = ["complexity_agent", "structure_agent"]

    def supervisor_node(state: AgentState) -> AgentState:
        """
        Nó do supervisor que decide qual agente deve agir a seguir.

        Args:
            state (AgentState): Estado atual do sistema

        Returns:
            AgentState: Estado atualizado com o próximo agente a ser executado
        """
        logger.info("Supervisor avaliando estado...")
        finished = state.get("finished_agents", [])
        logger.info(f"Agentes finalizados: {finished} ({len(finished)}/{len(members)})")

        if len(finished) >= len(members):
            logger.info("Todos os agentes finalizados. Retornando FINISH.")
            return {"next": "FINISH"}

        for agent in members:
            if agent not in finished:
                logger.info(f"Próximo agente selecionado: {agent}")
                return {"next": agent}

        logger.info("Nenhum agente restante. Retornando FINISH.")
        return {"next": "FINISH"}

    def complexity_node(state: AgentState) -> AgentState:
        """
        Executa o agente de análise de complexidade.

        Args:
            state (AgentState): Estado atual do sistema

        Returns:
            AgentState: Estado atualizado após análise de complexidade
        """
        try:
            logger.info("➡️  Iniciando complexity_agent...")
            code = state.get("python_code", "")
            logger.info(f"Código a analisar: {len(code)} caracteres")

            messages = [
                HumanMessage(
                    content=f"""Analise o código Python abaixo em busca de problemas de COMPLEXIDADE.

                    IMPORTANTE: Use a ferramenta analyze_cyclomatic_complexity passando EXATAMENTE o código completo que está abaixo.
                    Não modifique, não extraia trechos, passe TODO o código como está.

                    CÓDIGO PYTHON:
                    ```python
                    {code}
                    ```"""
                )
            ]
            logger.info(f"Mensagem criada: {len(messages)} mensagem(ns)")

            logger.info("Invocando complexity_agent...")
            result = complexity_agent.invoke({"messages": messages})
            logger.info(
                f"Complexity_agent respondeu: {len(result.get('messages', []))} mensagens"
            )

            finished = state.get("finished_agents", [])
            finished.append("complexity_agent")
            logger.info(f"Complexity_agent finalizado. Agentes finalizados: {finished}")

            return {
                "messages": result["messages"],
                "finished_agents": finished,
            }
        except Exception as e:
            logger.error(f"Tipo: {type(e).__name__}")
            logger.error(f"Mensagem: {str(e)}")
            logger.error("Traceback:")
            logger.error(traceback.format_exc())
            raise

    def structure_node(state: AgentState) -> AgentState:
        """
        Executa o agente de análise de estrutura.

        Args:
            state (AgentState): Estado atual do sistema

        Returns:
            AgentState: Estado atualizado após análise de estrutura
        """
        try:
            logger.info("➡️  Iniciando structure_agent...")
            code = state.get("python_code", "")
            logger.info(f"Código a analisar: {len(code)} caracteres")

            messages = [
                HumanMessage(
                    content=f"""Analise o código Python abaixo em busca de problemas de ESTRUTURA. IMPORTANTE: Use as ferramentas disponíveis passando EXATAMENTE o código completo que está abaixo. Não modifique, não extraia trechos, passe TODO o código como está.
                    CÓDIGO PYTHON:
                    ```python
                    {code}
                    ```"""
                )
            ]
            logger.info(f"Mensagem criada: {len(messages)} mensagem(ns)")

            logger.info("Invocando structure_agent...")

            result = structure_agent.invoke({"messages": messages})

            logger.info(
                f"Structure_agent respondeu: {len(result.get('messages', []))} mensagens"
            )

            finished = state.get("finished_agents", [])
            finished.append("structure_agent")
            logger.info(f"Structure_agent finalizado. Agentes finalizados: {finished}")

            return {
                "messages": result["messages"],
                "finished_agents": finished,
            }
        except Exception as e:
            logger.error(f"Mensagem: {str(e)}")
            logger.error("Traceback:")
            logger.error(traceback.format_exc())
            raise

    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("complexity_agent", complexity_node)
    workflow.add_node("structure_agent", structure_node)

    def router(state: AgentState) -> str:
        """
        Roteia para o próximo nó baseado no estado.

        Args:
            state (AgentState): Estado atual do sistema

        Returns:
            str: Nome do próximo nó a ser executado
        """
        next_agent = state.get("next", "FINISH")
        if next_agent == "FINISH":
            return END
        return next_agent

    workflow.add_edge("complexity_agent", "supervisor")
    workflow.add_edge("structure_agent", "supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        router,
        {
            "complexity_agent": "complexity_agent",
            "structure_agent": "structure_agent",
            END: END,
        },
    )

    workflow.set_entry_point("supervisor")

    return workflow.compile()
