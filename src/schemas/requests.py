from pydantic import BaseModel, Field


class AnalyzeCodeRequest(BaseModel):
    """
    Schema para requisição de análise de código

    Attributes:
        code: Código Python a ser analisado
        file_name: Nome do arquivo (opcional)
    """

    code: str = Field(..., description="Código Python a ser analisado")
    file_name: str | None = Field(default=None, description="Nome do arquivo (opcional)")


class AnalyzeCodeResponse(BaseModel):
    """
    Schema para resposta de análise de código

    Attributes:
        success: Indica se a análise foi bem sucedida
        message: Mensagem de status
        code_smells: Lista de code smells encontrados
    """

    success: bool = Field(..., description="Indica se a análise foi bem sucedida")
    message: str = Field(..., description="Mensagem de status")
    code_smells: list = Field(default_factory=list, description="Code smells encontrados")
