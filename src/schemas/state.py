import operator
from typing import Annotated, Any, Dict, List, TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict, total=False):
    """Estado compartilhado entre todos os agentes"""

    messages: Annotated[List[BaseMessage], operator.add]
    python_code: str
    file: str | None
    code_smells: Annotated[List[Dict[str, Any]], operator.add]
    next: str
    finished_agents: List[str]
