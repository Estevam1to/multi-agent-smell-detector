import os
import shutil
import subprocess
import tempfile
import json
import yaml

class FileProcessor:
    def __init__(self, base_dir="/tmp/uploads", temp_dir="/tmp/processing"):
        self.base_dir = base_dir
        self.temp_dir = temp_dir
        self.processed_files = []
        self.error_log = []
        self.config = {"allowed_extensions": [".txt", ".csv", ".json", ".yml"]}
        
        # Create directories if they don't exist
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def read_file(self, filename):
        # Path traversal vulnerability - allows reading files outside base_dir
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            with open(filepath, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            self.error_log.append(f"Error reading {filename}: {str(e)}")
            return None
    
    def write_file(self, filename, content):
        # Path traversal vulnerability in write operations
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            with open(filepath, 'w') as file:
                file.write(content)
            self.processed_files.append(filename)
            return True
        except Exception as e:
            self.error_log.append(f"Error writing {filename}: {str(e)}")
            return False
    
    def process_yaml_file(self, filename):
        # Unsafe YAML loading (security smell)
        content = self.read_file(filename)
        if content:
            try:
                # Unsafe YAML loading can lead to arbitrary code execution
                data = yaml.load(content, Loader=yaml.Loader)
                return data
            except Exception as e:
                self.error_log.append(f"Error parsing YAML {filename}: {str(e)}")
        return None
    
    def process_json_file(self, filename):
        content = self.read_file(filename)
        if content:
            try:
                data = json.loads(content)
                return data
            except Exception as e:
                self.error_log.append(f"Error parsing JSON {filename}: {str(e)}")
        return None
    
    def convert_file_format(self, input_filename, output_format):
        # Command injection vulnerability
        if output_format not in ["txt", "json", "csv", "xml"]:
            self.error_log.append(f"Unsupported output format: {output_format}")
            return False
        
        input_path = os.path.join(self.base_dir, input_filename)
        output_filename = os.path.splitext(input_filename)[0] + "." + output_format
        output_path = os.path.join(self.base_dir, output_filename)
        
        # Command injection vulnerability
        cmd = f"convert {input_path} {output_path}"
        try:
            # Unsafe subprocess call with shell=True
            subprocess.run(cmd, shell=True, check=True)
            self.processed_files.append(output_filename)
            return True
        except subprocess.CalledProcessError as e:
            self.error_log.append(f"Error converting {input_filename}: {str(e)}")
            return False
    
    def cleanup_old_files(self, max_age_days=7):
        # Long method with too many responsibilities (code smell)
        current_time = os.time.time()
        count_removed = 0
        count_errors = 0
        
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                file_age = current_time - os.path.getmtime(filepath)
                age_in_days = file_age / (60 * 60 * 24)
                
                if age_in_days > max_age_days:
                    try:
                        os.remove(filepath)
                        count_removed += 1
                    except Exception as e:
                        self.error_log.append(f"Error removing old file {filepath}: {str(e)}")
                        count_errors += 1
        
        # Also clean up temp directory
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                filepath = os.path.join(root, file)
                file_age = current_time - os.path.getmtime(filepath)
                age_in_days = file_age / (60 * 60 * 24)
                
                if age_in_days > 1:  # More aggressive cleanup for temp files
                    try:
                        os.remove(filepath)
                        count_removed += 1
                    except Exception as e:
                        self.error_log.append(f"Error removing temp file {filepath}: {str(e)}")
                        count_errors += 1
        
        return {"removed": count_removed, "errors": count_errors}
