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
