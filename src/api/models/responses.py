"""Modelos de resposta da API."""

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    total_smells_detected: int
    code_smells: list[dict]
    agents_executed: int
