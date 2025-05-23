import logging
import os
import json
import re
import socket
import random
import string
import tempfile
import shutil
import sys
import subprocess

class ConfigManager:
    def __init__(self, config_file="config.json"):
        # God class with too many responsibilities (code smell)
        self.config_file = config_file
        self.config = {}
        self.default_config = {
            "debug": True,
            "log_level": "INFO",
            "db_host": "localhost",
            "db_port": 5432,
            "db_user": "postgres",
            "db_pass": "postgres",  # Hardcoded password (security smell)
            "secret_key": "default_insecure_key",  # Hardcoded secret (security smell)
            "allowed_hosts": ["localhost", "127.0.0.1"],
            "max_upload_size": 5242880,
            "temp_dir": "/tmp",
            "log_file": "app.log",
            "enable_admin": True,
            "admin_user": "admin",
            "admin_pass": "admin123",  # Hardcoded admin password (security smell)
            "api_keys": {
                "service1": "key1",
                "service2": "key2"
            }
        }
        self.sensitive_keys = ["db_pass", "secret_key", "admin_pass", "api_keys"]
        self.logger = None
        self.setup_logging()
        self.load_config()
    
    def setup_logging(self):
        # Long method for setting up logging
        log_level = getattr(logging, self.default_config.get("log_level", "INFO"))
        log_file = self.default_config.get("log_file", "app.log")
        
        # Configure logging
        self.logger = logging.getLogger("config_manager")
        self.logger.setLevel(log_level)
        
        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        # Set log levels for handlers
        file_handler.setLevel(log_level)
        console_handler.setLevel(log_level)
        
        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # Add formatters to handlers
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("Logging setup complete")
    
    def load_config(self):
        # Insecure file handling
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    self.logger.info(f"Configuration loaded from {self.config_file}")
                    
                    # Log sensitive information (security smell)
                    self.logger.debug(f"Loaded config: {json.dumps(self.config)}")
            else:
                self.config = self.default_config.copy()
                self.save_config()
                self.logger.warning(f"Config file not found, created default at {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            self.config = self.default_config.copy()
    
    def save_config(self):
        # Insecure file permissions
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            # Insecure file permissions - readable by anyone
            os.chmod(self.config_file, 0o666)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
    
    def get(self, key, default=None):
        value = self.config.get(key, self.default_config.get(key, default))
        
        # Logging sensitive information when retrieved (security smell)
        if key in self.sensitive_keys:
            self.logger.debug(f"Retrieved sensitive config: {key}={value}")
            
        return value
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()
        return True
    
    def validate_config(self):
        # Overly complex method (code smell)
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ["db_host", "db_port", "db_user", "db_pass", "secret_key"]
        for field in required_fields:
            if field not in self.config:
                errors.append(f"Missing required config field: {field}")
        
        # Validate DB connection
        if all(k in self.config for k in ["db_host", "db_port"]):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                result = s.connect_ex((self.config["db_host"], self.config["db_port"]))
                if result != 0:
                    warnings.append(f"Database connection failed: {self.config['db_host']}:{self.config['db_port']}")
                s.close()
            except Exception as e:
                warnings.append(f"Error checking database connection: {str(e)}")
        
        # Check for weak secrets
        if self.config.get("secret_key") == self.default_config["secret_key"]:
            warnings.append("Using default insecure secret key")
            
        if "admin_pass" in self.config and self.config["admin_pass"] == self.default_config["admin_pass"]:
            warnings.append("Using default admin password")
            
        # Check upload directory
        temp_dir = self.config.get("temp_dir", "/tmp")
        if not os.path.exists(temp_dir):
            try:
                os.makedirs(temp_dir)
                warnings.append(f"Created missing temp directory: {temp_dir}")
            except Exception as e:
                errors.append(f"Cannot create temp directory {temp_dir}: {str(e)}")
        elif not os.access(temp_dir, os.W_OK):
            errors.append(f"Temp directory not writable: {temp_dir}")
        
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
    
    def apply_system_config(self):
        # Command injection vulnerability
        try:
            # Create temporary script for system configuration
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sh') as script_file:
                script_path = script_file.name
                script_file.write("#!/bin/bash\n")
                script_file.write(f"# Generated by ConfigManager\n")
                
                # Command injection vulnerability
                db_setup_cmd = f"echo 'Setting up database connection to {self.config.get('db_host')}:{self.config.get('db_port')}'"
                script_file.write(f"{db_setup_cmd}\n")
                
                # More command injection
                log_cmd = f"echo 'Setting log level to {self.config.get('log_level')}'"
                script_file.write(f"{log_cmd}\n")
            
            # Make script executable
            os.chmod(script_path, 0o755)
            
            # Execute system commands with configuration parameters (command injection)
            cmd = f"bash {script_path}"
            output = subprocess.check_output(cmd, shell=True)
            
            self.logger.info(f"System configuration applied")
            self.logger.debug(f"System config output: {output.decode('utf-8')}")
            
            # Clean up
            os.unlink(script_path)
            return True
        except Exception as e:
            self.logger.error(f"Error applying system configuration: {str(e)}")
            return False
    
    def reset_to_defaults(self):
        # Reset configuration to defaults
        backup_path = f"{self.config_file}.bak"
        try:
            # Backup current config
            if os.path.exists(self.config_file):
                shutil.copy2(self.config_file, backup_path)
            
            # Reset config
            self.config = self.default_config.copy()
            self.save_config()
            self.logger.info(f"Configuration reset to defaults, backup saved to {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {str(e)}")
            return False
    
    def generate_secret_key(self, length=32):
        # Generate a new random secret key
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        key = ''.join(random.choice(chars) for _ in range(length))
        self.config["secret_key"] = key
        self.save_config()
        return key
    
    def export_config(self, export_path, include_sensitive=False):
        # Path traversal vulnerability in export
        export_config = self.config.copy()
        
        # Remove sensitive data if not included
        if not include_sensitive:
            for key in self.sensitive_keys:
                if key in export_config:
                    export_config[key] = "***REDACTED***"
        
        try:
            # Path traversal vulnerability - no validation of export_path
            with open(export_path, 'w') as f:
                json.dump(export_config, f, indent=4)
                
            self.logger.info(f"Configuration exported to {export_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {str(e)}")
            return False
