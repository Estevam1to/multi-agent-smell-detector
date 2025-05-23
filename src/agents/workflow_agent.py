import json
import os
from pathlib import Path
import subprocess
import tempfile
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor import create_supervisor
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


def run_bandit_tool(code: str) -> list:
    """
    Runs Bandit on Python code and returns the formatted results.
    Fixes the 'CalledProcessError' issue when vulnerabilities are found.

    Args:
        code (str): Python code to be analyzed.

    Returns:
        List[Dict]: List of found vulnerabilities (empty if none).
    """
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            ["bandit", "-f", "json", temp_file_path],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stdout:
            bandit_output = json.loads(result.stdout)
            return bandit_output.get("results", [])
        return []

    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON do Bandit. STDERR: {result.stderr}")
        return []
    finally:
        Path(temp_file_path).unlink(missing_ok=True)


llm_with_badit = llm.bind_tools([run_bandit_tool])
llm_with_analize_code = llm.bind_tools([analyze_code])


static_agent = create_react_agent(
    name="static-analizer-agent",
    model=llm_with_analize_code,
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


security_agent = create_react_agent(
    name="security-agent",
    model=llm_with_badit,
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


supervisor = create_supervisor(
    agents=[static_agent, security_agent],
    model=llm,
    tools=[],
    prompt="""You are the Agent Supervisor. Your role is to monitor and validate the output of static and security agents, ensuring:

    1. **Functionality**: Verify that each agent correctly fulfilled its task.
    2. **Security**: Identify and remediate security vulnerabilities in the code.
    3. **Quality**: Detect and fix code smells and poor practices.
    4. **Feedback**: For each agent:
    - If correct, confirm success and move to the next task.
    - If there is a failure or risk, present:
        a) Problem diagnosis.
        b) Adjusted code or clear instructions for correction.

    **Response format**:
    - List the verified points (Functionality, Security, Quality).
    - Include, when necessary, corrected code snippets.
    - End with next steps instructions or recommendations.

    Be objective, structured, and maintain a collaborative tone.
    """,
)

app = supervisor.compile()

response = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
import requests
import json
import os
import base64
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlencode

class APIClient:
    def __init__(self):
        self.base_url = "https://api.example.com"
        self.api_key = "1234567890abcdef"  
        self.username = "admin"
        self.password = "admin123"  
        self.token = None
        self.session = requests.Session()
        self.cache = {}
        self.debug = True
        self.timeout = 30
        self.retry_attempts = 3
        self.last_response = None
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "MyApp/1.0",
            "X-API-Key": self.api_key 
        }
    
    def authenticate(self):
        auth_url = f"{self.base_url}/auth"
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = self.session.post(auth_url, json=payload, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            self.headers["Authorization"] = f"Bearer {self.token}"
            return True
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False
    
    def get_data(self, endpoint, params=None):

        if params is None:
            params = {}
        

        url = f"{self.base_url}/{endpoint}"
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"
        
        cache_key = url
        if cache_key in self.cache:
            if self.debug:
                print(f"Cache hit for: {url}")
            return self.cache[cache_key]
        
        tries = 0
        while tries < self.retry_attempts:
            try:
                response = self.session.get(url, headers=self.headers, timeout=self.timeout)
                self.last_response = response
                
                if response.status_code == 200:
                    if self.debug:
                        print(f"Response: {response.text}") 
                
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        data = response.json()
                    elif "application/xml" in content_type:
                        data = ET.fromstring(response.text)
                    else:
                        data = response.text
                    
                    self.cache[cache_key] = data
                    return data
                elif response.status_code == 401:
                    self.authenticate()
                    tries += 1
                else:
                    print(f"API error: {response.status_code} - {response.text}")
                    return None
            except requests.RequestException as e:
                print(f"Request failed: {str(e)}")
                tries += 1
                if tries >= self.retry_attempts:
                    return None
    
    def post_data(self, endpoint, data, raw_data=False):
        url = f"{self.base_url}/{endpoint}"
        
        payload = data
        if not raw_data and isinstance(data, dict):
            payload = json.dumps(data)
        
        try:
            response = self.session.post(url, data=payload, headers=self.headers, timeout=self.timeout)
            self.last_response = response
            response.raise_for_status()
            
            if self.debug:
                print(f"Posted data to {url}")
                print(f"Response: {response.text}")  
            return response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
        except Exception as e:
            print(f"Failed to post data: {str(e)}")
            return None
    
    def download_file(self, endpoint, params, output_path):
        url = f"{self.base_url}/{endpoint}"
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=self.timeout, stream=True)
            self.last_response = response
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return True
        except Exception as e:
            print(f"Failed to download file: {str(e)}")
            return False
    
    def process_xml_response(self, xml_string):
        try:
            parser = ET.XMLParser()
            root = ET.fromstring(xml_string, parser=parser)  
            
            result = {"data": []}
            for element in root.findall(".//item"):
                item_data = {}
                for child in element:
                    item_data[child.tag] = child.text
                result["data"].append(item_data)
                
            return result
        except Exception as e:
            print(f"XML processing error: {str(e)}")
            return None
    
    def execute_remote_command(self, command, params):
        endpoint = f"execute/{command}"
        command_str = command
        
        if params:
            for key, value in params.items():
                command_str += f" {key}={value}"
        
        try:
            result = subprocess.check_output(command_str, shell=True)
            return {"output": result.decode("utf-8")}
        except subprocess.CalledProcessError as e:
            return {"error": str(e), "output": e.output.decode("utf-8") if e.output else ""}
    
    def clear_cache(self):
        self.cache = {}
        print("Cache cleared")

                """,
            }
        ]
    }
)

print(response)
