"""
LLM as a Judge - Sistema de avaliação automática usando LLM.

Este módulo implementa um juiz baseado em LLM que avalia se os agentes
detectaram corretamente os code smells nos casos de teste.
"""

import json
from typing import Dict, List

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from config.settings import settings


class LLMJudge:
    """
    LLM Judge que avalia a qualidade das detecções de code smells.

    Usa um LLM para determinar se os agentes detectaram corretamente
    os code smells esperados.
    """

    def __init__(self):
        """Inicializa o LLM Judge."""
        self.model = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0,
        )

        self.judge_prompt = """Você é um juiz especializado em avaliar detecções de code smells em Python.

Sua tarefa é avaliar se um agente de detecção identificou corretamente um code smell em um código.

Você receberá:
1. O código Python analisado
2. O tipo de smell esperado
3. A resposta do agente
4. Metadados sobre o smell esperado

Você deve avaliar:
- Se o agente detectou o smell quando deveria (True Positive)
- Se o agente não detectou o smell quando não deveria (True Negative)
- Se o agente detectou algo que não existe (False Positive)
- Se o agente não detectou algo que existe (False Negative)

Responda APENAS com um JSON no seguinte formato:
{
    "verdict": "TP" | "TN" | "FP" | "FN",
    "confidence": 0.0-1.0,
    "reasoning": "Explicação detalhada da sua decisão",
    "smell_correctly_identified": true | false,
    "details_accuracy": "low" | "medium" | "high"
}

Legenda:
- TP (True Positive): Smell existe e foi detectado corretamente
- TN (True Negative): Smell não existe e não foi detectado
- FP (False Positive): Smell não existe mas foi detectado
- FN (False Negative): Smell existe mas não foi detectado
"""

    async def evaluate_detection(
        self,
        code: str,
        smell_type: str,
        agent_response: str,
        expected_detection: bool,
        metadata: Dict = None,
    ) -> Dict:
        """
        Avalia se a detecção do agente foi correta.

        Args:
            code: Código Python analisado
            smell_type: Tipo de smell esperado
            agent_response: Resposta do agente
            expected_detection: Se o smell deveria ser detectado
            metadata: Metadados adicionais sobre o smell

        Returns:
            Dicionário com o veredicto do juiz
        """
        evaluation_prompt = f"""
{self.judge_prompt}

## CÓDIGO ANALISADO:
```python
{code}
```

## TIPO DE SMELL ESPERADO:
{smell_type}

## DETECÇÃO ESPERADA:
{"Sim, o smell DEVE ser detectado" if expected_detection else "Não, o smell NÃO deve ser detectado (código limpo)"}

## METADADOS DO SMELL:
{json.dumps(metadata, indent=2) if metadata else "Nenhum"}

## RESPOSTA DO AGENTE:
{agent_response}

## SUA AVALIAÇÃO (JSON):
"""

        # Executa o LLM Judge
        response = await self.model.ainvoke([HumanMessage(content=evaluation_prompt)])

        # Parse da resposta JSON
        try:
            # Extrai JSON da resposta
            content = response.content
            # Remove markdown code blocks se existirem
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            verdict = json.loads(content.strip())
            verdict["raw_response"] = response.content
            return verdict
        except json.JSONDecodeError as e:
            return {
                "verdict": "ERROR",
                "confidence": 0.0,
                "reasoning": f"Erro ao parsear resposta do juiz: {str(e)}",
                "smell_correctly_identified": False,
                "details_accuracy": "low",
                "raw_response": response.content,
            }

    async def evaluate_test_suite(
        self, test_results: List[Dict]
    ) -> Dict[str, any]:
        """
        Avalia um conjunto completo de testes.

        Args:
            test_results: Lista de resultados de testes

        Returns:
            Dicionário com métricas agregadas
        """
        evaluations = []

        for test in test_results:
            evaluation = await self.evaluate_detection(
                code=test["code"],
                smell_type=test["smell_type"],
                agent_response=test["agent_response"],
                expected_detection=test["expected_detection"],
                metadata=test.get("metadata"),
            )

            evaluations.append(
                {
                    "test_name": test.get("name", "Unknown"),
                    "smell_type": test["smell_type"],
                    **evaluation,
                }
            )

        # Calcula métricas
        tp = sum(1 for e in evaluations if e["verdict"] == "TP")
        tn = sum(1 for e in evaluations if e["verdict"] == "TN")
        fp = sum(1 for e in evaluations if e["verdict"] == "FP")
        fn = sum(1 for e in evaluations if e["verdict"] == "FN")
        errors = sum(1 for e in evaluations if e["verdict"] == "ERROR")

        total = tp + tn + fp + fn
        accuracy = (tp + tn) / total if total > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        return {
            "total_tests": len(evaluations),
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
            },
            "confusion_matrix": {
                "true_positives": tp,
                "true_negatives": tn,
                "false_positives": fp,
                "false_negatives": fn,
                "errors": errors,
            },
            "detailed_evaluations": evaluations,
        }


# Instância global do juiz
_judge_instance = None


def get_judge() -> LLMJudge:
    """
    Retorna a instância singleton do LLM Judge.

    Returns:
        Instância do LLMJudge
    """
    global _judge_instance
    if _judge_instance is None:
        _judge_instance = LLMJudge()
    return _judge_instance
