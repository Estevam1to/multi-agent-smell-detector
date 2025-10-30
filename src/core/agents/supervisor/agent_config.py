"""Configuração dos agentes especializados."""

from core.prompts.complex_conditional_prompt import COMPLEX_CONDITIONAL_AGENT_PROMPT
from core.prompts.complex_method_prompt import COMPLEX_METHOD_AGENT_PROMPT
from core.prompts.empty_catch_block_prompt import EMPTY_CATCH_BLOCK_AGENT_PROMPT
from core.prompts.long_identifier_prompt import LONG_IDENTIFIER_AGENT_PROMPT
from core.prompts.long_lambda_function_prompt import LONG_LAMBDA_FUNCTION_AGENT_PROMPT
from core.prompts.long_message_chain_prompt import LONG_MESSAGE_CHAIN_AGENT_PROMPT
from core.prompts.long_method_prompt import LONG_METHOD_AGENT_PROMPT
from core.prompts.long_parameter_list_prompt import LONG_PARAMETER_LIST_AGENT_PROMPT
from core.prompts.long_statement_prompt import LONG_STATEMENT_AGENT_PROMPT
from core.prompts.magic_number_prompt import MAGIC_NUMBER_AGENT_PROMPT
from core.prompts.missing_default_prompt import MISSING_DEFAULT_AGENT_PROMPT
from core.schemas.agent_response import (
    ComplexConditionalDetection,
    ComplexMethodDetection,
    EmptyCatchBlockDetection,
    LongIdentifierDetection,
    LongLambdaFunctionDetection,
    LongMessageChainDetection,
    LongMethodDetection,
    LongParameterListDetection,
    LongStatementDetection,
    MagicNumberDetection,
    MissingDefaultDetection,
)

AGENT_CONFIGS = {
    "complex_method": {
        "prompt": COMPLEX_METHOD_AGENT_PROMPT,
        "schema": ComplexMethodDetection,
    },
    "long_method": {
        "prompt": LONG_METHOD_AGENT_PROMPT,
        "schema": LongMethodDetection,
    },
    "complex_conditional": {
        "prompt": COMPLEX_CONDITIONAL_AGENT_PROMPT,
        "schema": ComplexConditionalDetection,
    },
    "long_parameter_list": {
        "prompt": LONG_PARAMETER_LIST_AGENT_PROMPT,
        "schema": LongParameterListDetection,
    },
    "long_statement": {
        "prompt": LONG_STATEMENT_AGENT_PROMPT,
        "schema": LongStatementDetection,
    },
    "long_identifier": {
        "prompt": LONG_IDENTIFIER_AGENT_PROMPT,
        "schema": LongIdentifierDetection,
    },
    "magic_number": {
        "prompt": MAGIC_NUMBER_AGENT_PROMPT,
        "schema": MagicNumberDetection,
    },
    "empty_catch_block": {
        "prompt": EMPTY_CATCH_BLOCK_AGENT_PROMPT,
        "schema": EmptyCatchBlockDetection,
    },
    "missing_default": {
        "prompt": MISSING_DEFAULT_AGENT_PROMPT,
        "schema": MissingDefaultDetection,
    },
    "long_lambda_function": {
        "prompt": LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
        "schema": LongLambdaFunctionDetection,
    },
    "long_message_chain": {
        "prompt": LONG_MESSAGE_CHAIN_AGENT_PROMPT,
        "schema": LongMessageChainDetection,
    },
}
