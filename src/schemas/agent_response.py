"""
Schemas Pydantic para respostas estruturadas dos agentes.

Define o formato de saída JSON que cada agente deve retornar.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class SmellDetection(BaseModel):
    """Schema base para detecção de um code smell."""

    detected: bool = Field(
        description="Se o code smell foi detectado ou não"
    )
    smell_type: str = Field(
        description="Tipo do code smell (long_method, complex_method, etc.)"
    )
    severity: str = Field(
        description="Severidade do smell: low, medium, high",
        default="medium"
    )


class LongMethodDetection(SmellDetection):
    """Detecção de Long Method."""

    smell_type: str = "long_method"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que é muito longo"
    )
    line_start: Optional[int] = Field(
        default=None,
        description="Linha onde o método começa"
    )
    line_end: Optional[int] = Field(
        default=None,
        description="Linha onde o método termina"
    )
    total_lines: Optional[int] = Field(
        default=None,
        description="Total de linhas do método"
    )
    threshold: int = Field(
        default=67,
        description="Limite máximo de linhas recomendado"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class ComplexMethodDetection(SmellDetection):
    """Detecção de Complex Method."""

    smell_type: str = "complex_method"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método complexo"
    )
    line_start: Optional[int] = Field(
        default=None,
        description="Linha onde o método começa"
    )
    line_end: Optional[int] = Field(
        default=None,
        description="Linha onde o método termina"
    )
    cyclomatic_complexity: Optional[int] = Field(
        default=None,
        description="Complexidade ciclomática calculada"
    )
    threshold: int = Field(
        default=7,
        description="Limite máximo de complexidade ciclomática"
    )
    decision_points: Optional[int] = Field(
        default=None,
        description="Número de pontos de decisão encontrados"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class ComplexConditionalDetection(SmellDetection):
    """Detecção de Complex Conditional."""

    smell_type: str = "complex_conditional"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que contém a condicional"
    )
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde está a condicional complexa"
    )
    logical_operators: Optional[int] = Field(
        default=None,
        description="Número de operadores lógicos (and, or)"
    )
    threshold: int = Field(
        default=2,
        description="Limite máximo de operadores lógicos"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class LongParameterListDetection(SmellDetection):
    """Detecção de Long Parameter List."""

    smell_type: str = "long_parameter_list"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método com muitos parâmetros"
    )
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde o método está definido"
    )
    parameter_count: Optional[int] = Field(
        default=None,
        description="Número de parâmetros"
    )
    threshold: int = Field(
        default=4,
        description="Limite máximo de parâmetros recomendado"
    )
    parameter_names: Optional[List[str]] = Field(
        default=None,
        description="Lista de nomes dos parâmetros"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class LongStatementDetection(SmellDetection):
    """Detecção de Long Statement."""

    smell_type: str = "long_statement"
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde está o statement longo"
    )
    line_length: Optional[int] = Field(
        default=None,
        description="Comprimento da linha em caracteres"
    )
    threshold: int = Field(
        default=80,
        description="Limite máximo de caracteres por linha"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class LongIdentifierDetection(SmellDetection):
    """Detecção de Long Identifier."""

    smell_type: str = "long_identifier"
    identifier_name: Optional[str] = Field(
        default=None,
        description="Nome do identificador muito longo"
    )
    identifier_type: Optional[str] = Field(
        default=None,
        description="Tipo: variable, function, class, etc."
    )
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde o identificador é definido"
    )
    length: Optional[int] = Field(
        default=None,
        description="Comprimento do identificador"
    )
    threshold: int = Field(
        default=20,
        description="Limite máximo de caracteres para identificador"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de nome mais curto"
    )


class MagicNumberDetection(SmellDetection):
    """Detecção de Magic Number."""

    smell_type: str = "magic_number"
    magic_numbers: Optional[List[float]] = Field(
        default=None,
        description="Lista de números mágicos encontrados"
    )
    line_numbers: Optional[List[int]] = Field(
        default=None,
        description="Linhas onde os números mágicos aparecem"
    )
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que contém os magic numbers"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de nomes de constantes"
    )


class EmptyCatchBlockDetection(SmellDetection):
    """Detecção de Empty Catch Block."""

    smell_type: str = "empty_catch_block"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que contém o bloco vazio"
    )
    line_start: Optional[int] = Field(
        default=None,
        description="Linha onde o try/except começa"
    )
    line_end: Optional[int] = Field(
        default=None,
        description="Linha onde o try/except termina"
    )
    exception_type: Optional[str] = Field(
        default=None,
        description="Tipo de exceção capturada"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de como tratar a exceção"
    )


class MissingDefaultDetection(SmellDetection):
    """Detecção de Missing Default."""

    smell_type: str = "missing_default"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que contém o match sem default"
    )
    line_start: Optional[int] = Field(
        default=None,
        description="Linha onde o match começa"
    )
    line_end: Optional[int] = Field(
        default=None,
        description="Linha onde o match termina"
    )
    cases_count: Optional[int] = Field(
        default=None,
        description="Número de cases no match"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de adicionar case default"
    )


class LongLambdaFunctionDetection(SmellDetection):
    """Detecção de Long Lambda Function."""

    smell_type: str = "long_lambda_function"
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde a lambda está definida"
    )
    lambda_length: Optional[int] = Field(
        default=None,
        description="Comprimento da lambda em caracteres"
    )
    threshold: int = Field(
        default=80,
        description="Limite máximo de caracteres para lambda"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de converter para função normal"
    )


class LongMessageChainDetection(SmellDetection):
    """Detecção de Long Message Chain."""

    smell_type: str = "long_message_chain"
    method_name: Optional[str] = Field(
        default=None,
        description="Nome do método que contém a chain"
    )
    line_number: Optional[int] = Field(
        default=None,
        description="Linha onde a chain está"
    )
    chain_length: Optional[int] = Field(
        default=None,
        description="Número de métodos encadeados"
    )
    threshold: int = Field(
        default=2,
        description="Limite máximo de métodos encadeados"
    )
    suggestion: Optional[str] = Field(
        default=None,
        description="Sugestão de refatoração"
    )


class AgentAnalysisResponse(BaseModel):
    """Schema para resposta completa de um agente."""

    agent_name: str = Field(
        description="Nome do agente que realizou a análise"
    )
    detections: List[SmellDetection] = Field(
        default_factory=list,
        description="Lista de code smells detectados"
    )
    analysis_summary: Optional[str] = Field(
        default=None,
        description="Resumo da análise realizada"
    )
