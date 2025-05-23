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
    Executa o Bandit no código Python e retorna os resultados formatados.
    Corrige o problema de 'CalledProcessError' quando vulnerabilidades são encontradas.

    Args:
        code (str): Código Python a ser analisado.

    Returns:
        List[Dict]: Lista de vulnerabilidades encontradas (vazia se nenhuma).
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


security_agent = create_react_agent(
    name="security-agent",
    model=llm_with_badit,
    tools=[run_bandit_tool],
    prompt="""Você é um especialista em segurança de aplicações Python. Sua tarefa é analisar o código abaixo, identificar vulnerabilidades de segurança e sugerir correções, utilizando a ferramenta **Bandit** para realizar a análise estática de segurança.
        Diretrizes:  
        1. Utilize a ferramenta Bandit para realizar a análise estática do código e identificar vulnerabilidades. Bandit é uma ferramenta que verifica vulnerabilidades comuns de segurança em código Python, como Execução Remota de Código (RCE), Injeção de SQL e Exposição de Dados Sensíveis.
        2. Priorize a detecção dos seguintes tipos de vulnerabilidades:
            - Execução Remota de Código (RCE)
            - Injeção de SQL
            - Exposição de Dados Sensíveis (Data Exposure)
        3. Para cada vulnerabilidade identificada, explique o risco em uma frase clara e objetiva (por exemplo: "SQL injection pode permitir acesso não autorizado ao banco de dados").
        4. Não altere o código do usuário.
        Retorne usando o seguinte formato:
        {
            "vulnerabilities": [
                {
                    "type": "Vulnerability Type",
                    "description": "Description of the vulnerability",
                    "risk": "Explique o risco em uma frase clara e objetiva",
                    "suggestion": "Sugestão de correção"
                    "code": "Código vulnerável",
                    "line": "Número da linha onde a vulnerabilidade foi encontrada"
                }
            ]
        }
    """,
)


supervisor = create_supervisor(
    agents=[static_agent, security_agent],
    model=llm,
    tools=[],
    prompt="""Você é o Supervisor de Agentes. Sua função é monitorar e validar a saída dos agentes estáticos e de segurança, assegurando:

    1. **Funcionalidade**: Verifique se cada agente cumpriu corretamente sua tarefa.
    2. **Segurança**: Identifique e remedie vulnerabilidades de segurança no código.
    3. **Qualidade**: Detecte e corrija code smells e práticas inadequadas.
    4. **Feedback**: Para cada agente:
    - Se estiver correto, confirme o sucesso e passe para a próxima tarefa.
    - Se houver falha ou risco, apresente:
        a) Diagnóstico do problema.  
        b) Código ajustado ou instruções claras para correção.

    **Formato de resposta**:
    - Liste os pontos verificados (Funcionalidade, Segurança, Qualidade).
    - Inclua, quando necessário, trechos de código corrigido.
    - Termine com uma instrução de próximos passos ou recomendação.

    Seja objetivo, estruturado e mantenha um tom colaborativo.
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
