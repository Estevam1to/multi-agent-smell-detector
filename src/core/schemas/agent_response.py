"""Schemas Pydantic para respostas estruturadas dos agentes."""

from typing import Optional
from pydantic import BaseModel, Field


class CodeSmellDetection(BaseModel):
    """Schema base para todas as detecções de code smell."""

    Project: str = Field(default="Code")
    Package: str = Field(default="Code")
    Module: str = Field(default="unknown")
    Class: str = Field(default="")
    Smell: str
    Method: str = Field(default="")
    Line_no: str = Field(default="")
    File: str = Field(default="")
    Description: str = Field(default="")

    detected: bool = Field(default=True)

    class Config:
        populate_by_name = True


class ComplexMethodDetection(CodeSmellDetection):
    Smell: str = Field(default="Complex method")
    cyclomatic_complexity: Optional[int] = None
    threshold: int = Field(default=7)


class LongMethodDetection(CodeSmellDetection):
    Smell: str = Field(default="Long method")
    total_lines: Optional[int] = None
    threshold: int = Field(default=67)


class ComplexConditionalDetection(CodeSmellDetection):
    Smell: str = Field(default="Complex conditional")
    logical_operators: Optional[int] = None
    threshold: int = Field(default=3)


class LongParameterListDetection(CodeSmellDetection):
    Smell: str = Field(default="Long parameter list")
    parameter_count: Optional[int] = None
    threshold: int = Field(default=4)


class LongStatementDetection(CodeSmellDetection):
    Smell: str = Field(default="Long statement")
    line_length: Optional[int] = None
    threshold: int = Field(default=80)


class LongIdentifierDetection(CodeSmellDetection):
    Smell: str = Field(default="Long identifier")
    identifier_name: Optional[str] = None
    length: Optional[int] = None
    threshold: int = Field(default=20)


class MagicNumberDetection(CodeSmellDetection):
    Smell: str = Field(default="Magic number")


class EmptyCatchBlockDetection(CodeSmellDetection):
    Smell: str = Field(default="Empty catch block")


class MissingDefaultDetection(CodeSmellDetection):
    Smell: str = Field(default="Missing default")


class LongLambdaFunctionDetection(CodeSmellDetection):
    Smell: str = Field(default="Long lambda function")
    lambda_length: Optional[int] = None
    threshold: int = Field(default=80)


class LongMessageChainDetection(CodeSmellDetection):
    Smell: str = Field(default="Long message chain")
    chain_length: Optional[int] = None
    threshold: int = Field(default=2)


class MultipleDetectionsResponse(BaseModel):
    """Wrapper para múltiplas detecções."""
    detections: list[CodeSmellDetection] = Field(default_factory=list)
    detected: bool = Field(default=False)


class MultipleLongIdentifierResponse(BaseModel):
    detections: list[LongIdentifierDetection] = Field(default_factory=list)
    detected: bool = Field(default=False)


class MultipleLongStatementResponse(BaseModel):
    detections: list[LongStatementDetection] = Field(default_factory=list)
    detected: bool = Field(default=False)
