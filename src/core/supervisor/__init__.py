"""Supervisor para coordenação de detecção de code smells."""

from .supervisor import CodeSmellSupervisor, analyze_code, get_supervisor

__all__ = ["CodeSmellSupervisor", "analyze_code", "get_supervisor"]
