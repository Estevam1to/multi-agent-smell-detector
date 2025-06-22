from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import Settings
from src.tools.bandit_tool import run_bandit_tool

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=Settings().API_KEY,
)


llm_with_bandit = llm.bind_tools([run_bandit_tool])


security_agent = create_react_agent(
    name="security-agent",
    model=llm_with_bandit,
    tools=[run_bandit_tool],
    prompt="""You are a Python application security expert. Your task is to analyze the code below, identify security vulnerabilities, and suggest fixes, using the **Bandit** tool for static security analysis.
        Guidelines:  
        1. Use the Bandit tool to perform static analysis of the code and identify vulnerabilities. Bandit is a tool that checks for common security vulnerabilities in Python code, such as Remote Code Execution (RCE), SQL Injection, and Sensitive Data Exposure.
        2. Prioritize the detection of the following vulnerability types:
            - Remote Code Execution (RCE)
            - SQL Injection
            - Sensitive Data Exposure
        3. For each identified vulnerability, explain the risk in a clear and objective sentence (for example: "SQL injection can allow unauthorized access to the database").
        4. Do not modify the user's code.
        Return using the following format:
        {
            "vulnerabilities": [
                {
                    "type": "Vulnerability Type",
                    "description": "Description of the vulnerability",
                    "risk": "Explain the risk in a clear and objective sentence",
                    "suggestion": "Suggestion for correction"
                    "code": "Vulnerable code",
                    "line": "Line number where the vulnerability was found"
                }
            ]
        }
    """,
)
