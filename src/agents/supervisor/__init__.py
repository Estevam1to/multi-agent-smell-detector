"""Supervisor agent para coordenação dos agentes especializados."""

from .supervisor_agent import (
    CodeSmellSupervisor,
    analyze_code_with_supervisor,
    get_supervisor,
)

from .supervisor_v2 import (
    CodeSmellSupervisorV2,
    analyze_code_with_supervisor_v2,
    get_supervisor_v2,
)

__all__ = [
    "CodeSmellSupervisor",
    "analyze_code_with_supervisor",
    "get_supervisor",
    "CodeSmellSupervisorV2",
    "analyze_code_with_supervisor_v2",
    "get_supervisor_v2",
]
