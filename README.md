# Static Analysis and Security for Python Code with AI Agents

This project implements specialized agents for static analysis and security of Python code using large language models (LLMs) and static analysis tools. These agents can detect code smells, security vulnerabilities, and provide improvement suggestions for Python code.

## Overview

The project consists of two main agents:

1. **Static Analyzer Agent**: Detects code smells such as God Classes, long methods, dead code, and cyclomatic complexity using Pylint.

2. **Security Agent**: Identifies security vulnerabilities such as Remote Code Execution (RCE), SQL injection, and sensitive data exposure using Bandit.

Additionally, there is a workflow agent that coordinates the two previous agents and generates combined reports.

## Project Structure

```
/tcc
├── README.md
├── src/
│   ├── agents/
│   │   ├── static_analizer_agent.py
│   │   ├── security_agent.py
│   │   ├── workflow_agent.py
```

## Requirements

- Python 3.8+
- Pylint
- Bandit
- LangGraph
- PydanticAI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tcc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install static analysis tools:
```bash
pip install pylint bandit
```

## Usage

### Using the Python Modules

You can use the agents directly in your Python code:

```python
# Example of using the Static Analyzer Agent
from src.agents.static_analizer_agent import static_agent

response = static_agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "your_python_code_here"}
        ]
    }
)
print(response["messages"][-1].content)
```

```python
# Example of using the Security Agent
from src.agents.security_agent import security_agent

response = security_agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "your_python_code_here"}
        ]
    }
)
print(response["messages"][-1].content)
```

```python
# Example of using the Workflow Agent
from src.agents.workflow_agent import app

response = app.invoke(
    {
        "messages": [
            {"role": "user", "content": "your_python_code_here"}
        ]
    }
)
print(response)
```

## Technologies Used

- **LangGraph**: Framework for LLM agent orchestration
- **PydanticAI**: Framework for defining agents and their interfaces
- **Pylint**: Static analysis tool for Python
- **Bandit**: Security analysis tool for Python
- **Gemini** and **Claude**: LLM models used by the agents

## Output Examples

### Static Analyzer Agent

The static analysis agent returns a JSON with detected code smells:

```json
{
    "code_smells": [
        {
            "type": "God Class",
            "description": "Class with too many attributes and responsibilities",
            "risk": "Makes maintenance difficult and violates the single responsibility principle",
            "suggestion": "Divide into multiple classes with specific responsibilities",
            "code": "class UserManager:",
            "line": 4
        }
    ]
}
```

### Security Agent

The security agent returns a JSON with detected vulnerabilities:

```json
{
    "vulnerabilities": [
        {
            "type": "Command Execution with Shell=True",
            "description": "Unsafe use of subprocess with shell=True",
            "risk": "May allow system command injection if input is not sanitized",
            "suggestion": "Replace with shell=False and pass arguments as a list",
            "code": "result = subprocess.run(pylint_cmd, shell=True, capture_output=True, text=True)",
            "line": 35
        }
    ]
}
```

## Contributions

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
