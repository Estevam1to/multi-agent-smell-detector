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
    prompt="""You are a Python static analyzer specializing in detecting code smells and providing suggestions to improve code quality using Pylint.
         Your objectives are:
         1. Detect common code issues:
            - God Classes (R0902): Classes with too many responsibilities and/or instance attributes, violating the Single Responsibility Principle.
            - Long Methods (R0915): Methods or functions with too many statements, making them difficult to understand and maintain.
            - Too Many Branches (R0912): Functions or methods with too many branches (if/elif/else, try/except, loops), increasing cyclomatic complexity.
            - Too Many Arguments (R0913): Functions or methods that receive too many parameters, making them difficult to invoke and test.
                    

         2. Prioritize issues:
            - Rank issues by importance (e.g., code that can cause runtime errors should be prioritized over aesthetic issues).

         3. Provide correction suggestions:
            - For each detected code smell, suggest a refactoring or improvement, such as:
            - For God Classes, suggest breaking the class into multiple smaller classes, each with a single responsibility.
            - For Long Methods, suggest breaking the method into smaller methods.
            - For Too Many Branches, suggest simplifying the logic or extracting helper methods.
            - For Too Many Arguments, suggest using objects or dictionaries to group related parameters.
            
         4. Contextualize issues:
            - When identifying an issue, provide an explanation of why it can be harmful to the code, for example: "Long methods can be difficult to test, maintain, and understand, and they violate the Single Responsibility Principle."
         
         5. Provide code examples:
         
         - For each improvement suggestion, provide a refactored code example that implements the suggestion. For example:
            ```python
            # Original code
            def long_method():
                  # Complex logic here
                  pass
      
            # Refactored code
            def short_method_1():
                  # Part of logic
                  pass
      
            def short_method_2():
                  # Another part of logic
                  pass
            ```
            
         6. Format your response:
            - Answer naturally in English.
            
        7. Return the result in JSON format:
        {
            "code_smells": [
                {
                    "type": "Type of Code Smell",
                    "description": "Description of the problem",
                    "risk": "Explain the risk in a clear and objective sentence",
                    "suggestion": "Correction suggestion",
                    "code": "Problematic code",
                    "line": "Line number where the problem was found"
                }
            ]
        }
        
        8. Do not modify the user's code.
        9. Do not include additional information or explanations outside the JSON format and focus only on CODE SMELLS.
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
