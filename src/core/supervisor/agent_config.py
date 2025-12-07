"""Configuração dos agentes especializados."""

# Imports para prompts simples
from core.simple_prompts.complex_conditional_prompt import (
    COMPLEX_CONDITIONAL_AGENT_PROMPT as SIMPLE_COMPLEX_CONDITIONAL_AGENT_PROMPT,
)
from core.simple_prompts.complex_method_prompt import (
    COMPLEX_METHOD_AGENT_PROMPT as SIMPLE_COMPLEX_METHOD_AGENT_PROMPT,
)
from core.simple_prompts.empty_catch_block_prompt import (
    EMPTY_CATCH_BLOCK_AGENT_PROMPT as SIMPLE_EMPTY_CATCH_BLOCK_AGENT_PROMPT,
)
from core.simple_prompts.long_identifier_prompt import (
    LONG_IDENTIFIER_AGENT_PROMPT as SIMPLE_LONG_IDENTIFIER_AGENT_PROMPT,
)
from core.simple_prompts.long_lambda_function_prompt import (
    LONG_LAMBDA_FUNCTION_AGENT_PROMPT as SIMPLE_LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
)
from core.simple_prompts.long_message_chain_prompt import (
    LONG_MESSAGE_CHAIN_AGENT_PROMPT as SIMPLE_LONG_MESSAGE_CHAIN_AGENT_PROMPT,
)
from core.simple_prompts.long_method_prompt import (
    LONG_METHOD_AGENT_PROMPT as SIMPLE_LONG_METHOD_AGENT_PROMPT,
)
from core.simple_prompts.long_parameter_list_prompt import (
    LONG_PARAMETER_LIST_AGENT_PROMPT as SIMPLE_LONG_PARAMETER_LIST_AGENT_PROMPT,
)
from core.simple_prompts.long_statement_prompt import (
    LONG_STATEMENT_AGENT_PROMPT as SIMPLE_LONG_STATEMENT_AGENT_PROMPT,
)
from core.simple_prompts.magic_number_prompt import (
    MAGIC_NUMBER_AGENT_PROMPT as SIMPLE_MAGIC_NUMBER_AGENT_PROMPT,
)
from core.simple_prompts.missing_default_prompt import (
    MISSING_DEFAULT_AGENT_PROMPT as SIMPLE_MISSING_DEFAULT_AGENT_PROMPT,
)

# Imports para prompts completos
from core.prompts.complex_conditional_prompt import (
    COMPLEX_CONDITIONAL_AGENT_PROMPT as COMPLETE_COMPLEX_CONDITIONAL_AGENT_PROMPT,
)
from core.prompts.complex_method_prompt import (
    COMPLEX_METHOD_AGENT_PROMPT as COMPLETE_COMPLEX_METHOD_AGENT_PROMPT,
)
from core.prompts.empty_catch_block_prompt import (
    EMPTY_CATCH_BLOCK_AGENT_PROMPT as COMPLETE_EMPTY_CATCH_BLOCK_AGENT_PROMPT,
)
from core.prompts.long_identifier_prompt import (
    LONG_IDENTIFIER_AGENT_PROMPT as COMPLETE_LONG_IDENTIFIER_AGENT_PROMPT,
)
from core.prompts.long_lambda_function_prompt import (
    LONG_LAMBDA_FUNCTION_AGENT_PROMPT as COMPLETE_LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
)
from core.prompts.long_message_chain_prompt import (
    LONG_MESSAGE_CHAIN_AGENT_PROMPT as COMPLETE_LONG_MESSAGE_CHAIN_AGENT_PROMPT,
)
from core.prompts.long_method_prompt import (
    LONG_METHOD_AGENT_PROMPT as COMPLETE_LONG_METHOD_AGENT_PROMPT,
)
from core.prompts.long_parameter_list_prompt import (
    LONG_PARAMETER_LIST_AGENT_PROMPT as COMPLETE_LONG_PARAMETER_LIST_AGENT_PROMPT,
)
from core.prompts.long_statement_prompt import (
    LONG_STATEMENT_AGENT_PROMPT as COMPLETE_LONG_STATEMENT_AGENT_PROMPT,
)
from core.prompts.magic_number_prompt import (
    MAGIC_NUMBER_AGENT_PROMPT as COMPLETE_MAGIC_NUMBER_AGENT_PROMPT,
)
from core.prompts.missing_default_prompt import (
    MISSING_DEFAULT_AGENT_PROMPT as COMPLETE_MISSING_DEFAULT_AGENT_PROMPT,
)

from core.schemas.agent_response import (
    MultipleComplexConditionalResponse,
    MultipleComplexMethodResponse,
    MultipleEmptyCatchBlockResponse,
    MultipleLongIdentifierResponse,
    MultipleLongLambdaResponse,
    MultipleLongMessageChainResponse,
    MultipleLongMethodResponse,
    MultipleLongParameterListResponse,
    MultipleLongStatementResponse,
    MultipleMagicNumberResponse,
    MultipleMissingDefaultResponse,
)


def get_agent_configs(prompt_type: str = "simple"):
    """
    Retorna configurações dos agentes baseado no tipo de prompt.
    
    Args:
        prompt_type: "simple" ou "complete"
    
    Returns:
        Dict com configurações dos agentes
    """
    if prompt_type == "complete":
        return {
            "complex_method": {
                "prompt": COMPLETE_COMPLEX_METHOD_AGENT_PROMPT,
                "schema": MultipleComplexMethodResponse,
            },
            "long_method": {
                "prompt": COMPLETE_LONG_METHOD_AGENT_PROMPT,
                "schema": MultipleLongMethodResponse,
            },
            "complex_conditional": {
                "prompt": COMPLETE_COMPLEX_CONDITIONAL_AGENT_PROMPT,
                "schema": MultipleComplexConditionalResponse,
            },
            "long_parameter_list": {
                "prompt": COMPLETE_LONG_PARAMETER_LIST_AGENT_PROMPT,
                "schema": MultipleLongParameterListResponse,
            },
            "long_statement": {
                "prompt": COMPLETE_LONG_STATEMENT_AGENT_PROMPT,
                "schema": MultipleLongStatementResponse,
            },
            "long_identifier": {
                "prompt": COMPLETE_LONG_IDENTIFIER_AGENT_PROMPT,
                "schema": MultipleLongIdentifierResponse,
            },
            "magic_number": {
                "prompt": COMPLETE_MAGIC_NUMBER_AGENT_PROMPT,
                "schema": MultipleMagicNumberResponse,
            },
            "empty_catch_block": {
                "prompt": COMPLETE_EMPTY_CATCH_BLOCK_AGENT_PROMPT,
                "schema": MultipleEmptyCatchBlockResponse,
            },
            "missing_default": {
                "prompt": COMPLETE_MISSING_DEFAULT_AGENT_PROMPT,
                "schema": MultipleMissingDefaultResponse,
            },
            "long_lambda_function": {
                "prompt": COMPLETE_LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
                "schema": MultipleLongLambdaResponse,
            },
            "long_message_chain": {
                "prompt": COMPLETE_LONG_MESSAGE_CHAIN_AGENT_PROMPT,
                "schema": MultipleLongMessageChainResponse,
            },
        }
    else:  # default: simple
        return {
            "complex_method": {
                "prompt": SIMPLE_COMPLEX_METHOD_AGENT_PROMPT,
                "schema": MultipleComplexMethodResponse,
            },
            "long_method": {
                "prompt": SIMPLE_LONG_METHOD_AGENT_PROMPT,
                "schema": MultipleLongMethodResponse,
            },
            "complex_conditional": {
                "prompt": SIMPLE_COMPLEX_CONDITIONAL_AGENT_PROMPT,
                "schema": MultipleComplexConditionalResponse,
            },
            "long_parameter_list": {
                "prompt": SIMPLE_LONG_PARAMETER_LIST_AGENT_PROMPT,
                "schema": MultipleLongParameterListResponse,
            },
            "long_statement": {
                "prompt": SIMPLE_LONG_STATEMENT_AGENT_PROMPT,
                "schema": MultipleLongStatementResponse,
            },
            "long_identifier": {
                "prompt": SIMPLE_LONG_IDENTIFIER_AGENT_PROMPT,
                "schema": MultipleLongIdentifierResponse,
            },
            "magic_number": {
                "prompt": SIMPLE_MAGIC_NUMBER_AGENT_PROMPT,
                "schema": MultipleMagicNumberResponse,
            },
            "empty_catch_block": {
                "prompt": SIMPLE_EMPTY_CATCH_BLOCK_AGENT_PROMPT,
                "schema": MultipleEmptyCatchBlockResponse,
            },
            "missing_default": {
                "prompt": SIMPLE_MISSING_DEFAULT_AGENT_PROMPT,
                "schema": MultipleMissingDefaultResponse,
            },
            "long_lambda_function": {
                "prompt": SIMPLE_LONG_LAMBDA_FUNCTION_AGENT_PROMPT,
                "schema": MultipleLongLambdaResponse,
            },
            "long_message_chain": {
                "prompt": SIMPLE_LONG_MESSAGE_CHAIN_AGENT_PROMPT,
                "schema": MultipleLongMessageChainResponse,
            },
        }


AGENT_CONFIGS = get_agent_configs("simple")
