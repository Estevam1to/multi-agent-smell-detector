"""Modelos de resposta da API."""

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    """Response com code smells detectados."""
    total_smells_detected: int
    code_smells: list[dict]
    agents_executed: int
