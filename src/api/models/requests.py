"""Modelos de requisição da API."""

from typing import Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    python_code: str
    file_path: Optional[str] = None
    project_name: str = "Code"
    use_structured_output: bool = False
