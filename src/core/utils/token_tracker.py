"""Utilitário para rastreamento de uso de tokens."""

from langchain_core.callbacks import AsyncCallbackHandler


def _extract_token_usage_from_llm_result(response) -> dict:
    """Extrai informações de uso de tokens de um LLMResult."""
    default_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    if hasattr(response, "llm_output") and response.llm_output:
        if "token_usage" in response.llm_output:
            usage = response.llm_output["token_usage"]
            return {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            }

    if hasattr(response, "generations"):
        for generation_list in response.generations:
            for generation in generation_list:
                if hasattr(generation, "message"):
                    message = generation.message

                    if hasattr(message, "response_metadata"):
                        metadata = message.response_metadata
                        if "token_usage" in metadata:
                            usage = metadata["token_usage"]
                            return {
                                "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0),
                                "total_tokens": usage.get("total_tokens", 0),
                            }
                        if "usage" in metadata:
                            usage = metadata["usage"]
                            return {
                                "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0),
                                "total_tokens": usage.get("total_tokens", 0),
                            }

                    if hasattr(message, "usage_metadata"):
                        usage = message.usage_metadata
                        if usage:
                            return {
                                "prompt_tokens": usage.get("input_tokens", 0),
                                "completion_tokens": usage.get("output_tokens", 0),
                                "total_tokens": usage.get("total_tokens", 0),
                            }

    return default_usage


class TokenUsageCallback(AsyncCallbackHandler):
    """Callback simples para capturar uso de tokens."""

    def __init__(self):
        super().__init__()
        self.token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    async def on_llm_end(self, response, **kwargs):
        """Captura uso de tokens quando a LLM termina."""
        self.token_usage = _extract_token_usage_from_llm_result(response)
