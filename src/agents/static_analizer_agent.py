import json
import os
import subprocess
import tempfile
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

API_KEY = os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=API_KEY,
)


def analyze_code(code: str) -> list:
    """Analyzes the provided Python code for specific code smells using Pylint.
    Returns a structured AnalysisResult object.
    Focuses only on:
    - God Classes (R0902)
    - Long Methods (C0301)
    - Dead Code (W0612)
    """
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp.write(code.encode("utf-8"))
        tmp_path = tmp.name

    try:
        enable_codes = "R0902,R0915,R0912,R0913"

        pylint_cmd = (
            f"pylint --exit-zero --output-format=json "
            f"--enable={enable_codes} "
            f"--disable=all "
            f"{tmp_path}"
        )

        result = subprocess.run(pylint_cmd, shell=True, capture_output=True, text=True)

        if result.stderr:
            print(f"Error running Pylint: {result.stderr}")
            return []

        pylint_output = json.loads(result.stdout) if result.stdout else []
        return pylint_output

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    finally:
        Path(tmp_path).unlink(missing_ok=True)


llm_with_bandit = llm.bind_tools([analyze_code])


static_agent = create_react_agent(
    name="static-analizer-agent",
    model=llm_with_bandit,
    tools=[analyze_code],
    prompt="""Você é um analisador estático especializado em Python, focado em detectar code smells e fornecer sugestões para melhorar a qualidade do código utilizando Pylint.
         Seu objetivo é:
         1. Detectar problemas comuns de código:
            - God Classes (R0902): Classes com muitas responsabilidades e/ou muitos atributos de instância, violando o princípio de responsabilidade única (Single Responsibility Principle).
            - Long Methods (R0915): Métodos ou funções com muitas instruções (statements), o que os torna difíceis de entender e manter.
            - Too Many Branches (R0912): Funções ou métodos com muitas ramificações (if/elif/else, try/except, loops), aumentando a complexidade ciclomática.
            - Too Many Arguments (R0913): Funções ou métodos que recebem muitos parâmetros, o que dificulta a sua invocação e a criação de testes.
                    

         2. Priorizar os problemas:
            - Classifique os problemas em ordem de importância (ex: código que pode causar erros de execução deve ser priorizado sobre problemas estéticos).

         3. Fornecer sugestões de correção:
            - Para cada code smell detectado, sugira uma refatoração ou uma melhoria, como por exemplo:
            - Para God Classes, sugerir a divisão da classe em várias classes menores, cada uma com uma responsabilidade única.
            - Para Long Methods, sugerir a divisão do método em métodos menores.
            - Para Too Many Branches, sugerir a simplificação da lógica ou a extração de métodos auxiliares.
            - Para Too Many Arguments, sugerir o uso de objetos ou dicionários para agrupar parâmetros relacionados.
            
         4. Contextualizar os problemas:
            - Ao identificar um problema, forneça uma explicação do porquê ele pode ser prejudicial ao código, por exemplo: "Métodos longos podem ser difíceis de testar, manter e entender, além de violarem o princípio da responsabilidade única."
         
         5. Fornecer exemplos de código:
         
         - Para cada sugestão de melhoria, forneça um exemplo de código refatorado que implemente a sugestão. Por exemplo:
            ```python
            # Código original
            def long_method():
                  # Lógica complexa aqui
                  pass
      
            # Código refatorado
            def short_method_1():
                  # Parte da lógica
                  pass
      
            def short_method_2():
                  # Outra parte da lógica
                  pass
            ```
            
         6. Limitar a resposta:
            - Reponda a reposta naturalmente em pt_br.
            
        7. Retornar o resultado em formato JSON:
        {
            "code_smells": [
                {
                    "type": "Tipo de Code Smell",
                    "description": "Descrição do problema",
                    "risk": "Explique o risco em uma frase clara e objetiva",
                    "suggestion": "Sugestão de correção",
                    "code": "Código problemático",
                    "line": "Número da linha onde o problema foi encontrado"
                }
            ]
        }
        
        8. Não altere o código do usuário.
        9. Não inclua informações adicionais ou explicações fora do formato JSON e foque apenas em CODE SMELLS.
        """,
)

response = static_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """

                """,
            }
        ]
    }
)

print(response["messages"][-1].content)
