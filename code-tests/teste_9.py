import os
import json
import time
import logging
import datetime
import csv
import random
import string
import re

class DataProcessor:
    """
    A God class that handles multiple responsibilities:
    - Data loading from multiple sources
    - Data transformation and processing
    - Data validation
    - Data export to multiple formats
    - Caching mechanism
    - Logging and metrics
    """
    
    def __init__(self, input_directory, output_directory, config_file=None, log_level="INFO"):
        # Too many instance variables
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.config_file = config_file
        self.config = {}
        self.data_cache = {}
        self.statistics = {
            "processed_files": 0,
            "successful_files": 0,
            "failed_files": 0,
            "processing_time": 0,
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "last_run": None
        }
        self.formats = ["csv", "json", "xml", "txt"]
        self.transformers = {}
        self.validators = {}
        self.exporters = {}
        self.allowed_fields = []
        self.required_fields = []
        self.field_types = {}
        self.max_cache_size = 1000
        self.cache_expiry = 3600
        self.enable_logging = True
        self.log_file = "data_processor.log"
        self.log_level = log_level
        self.last_error = None
        self.performance_metrics = {}
        
        # Initialize logging
        self._setup_logging()
        self._load_config()
        self._register_default_handlers()
    
    def _setup_logging(self):
        # Should be extracted to a dedicated logging service class
        level = getattr(logging, self.log_level)
        logging.basicConfig(
            filename=self.log_file,
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("DataProcessor")
        self.logger.info("DataProcessor initialized")
    
    def _load_config(self):
        # Should be extracted to a configuration service class
        if not self.config_file or not os.path.exists(self.config_file):
            self.logger.warning(f"Config file not found: {self.config_file}")
            return
            
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                
            # Apply configuration
            if 'allowed_fields' in self.config:
                self.allowed_fields = self.config['allowed_fields']
            if 'required_fields' in self.config:
                self.required_fields = self.config['required_fields']
            if 'field_types' in self.config:
                self.field_types = self.config['field_types']
            if 'max_cache_size' in self.config:
                self.max_cache_size = self.config['max_cache_size']
            if 'cache_expiry' in self.config:
                self.cache_expiry = self.config['cache_expiry']
                
            self.logger.info(f"Configuration loaded from {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            self.last_error = f"Config error: {str(e)}"
    
    def _register_default_handlers(self):
        # Register default transformers, validators, and exporters
        # This should be split into multiple methods
        
        # Register transformers
        self.transformers['lowercase'] = lambda x: x.lower() if isinstance(x, str) else x
        self.transformers['uppercase'] = lambda x: x.upper() if isinstance(x, str) else x
        self.transformers['trim'] = lambda x: x.strip() if isinstance(x, str) else x
        self.transformers['capitalize'] = lambda x: x.capitalize() if isinstance(x, str) else x
        
        # Register validators
        self.validators['not_empty'] = lambda x: x is not None and (not isinstance(x, str) or len(x) > 0)
        self.validators['is_numeric'] = lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit())
        self.validators['is_date'] = lambda x: bool(re.match(r'\d{4}-\d{2}-\d{2}', str(x))) if x else False
        
        # Register exporters
        self.exporters['csv'] = self._export_csv
        self.exporters['json'] = self._export_json
        
        self.logger.info("Default handlers registered")
    
    def process_data(self, input_files=None, output_format="json"):
        # Long method that does too much
        start_time = time.time()
        self.statistics['processed_files'] = 0
        self.statistics['successful_files'] = 0
        self.statistics['failed_files'] = 0
        self.statistics['total_records'] = 0
        self.statistics['valid_records'] = 0
        self.statistics['invalid_records'] = 0
        
        if input_files is None:
            # Get all files from input directory
            input_files = [f for f in os.listdir(self.input_directory) 
                          if os.path.isfile(os.path.join(self.input_directory, f))]
        
        if not input_files:
            self.logger.warning("No input files to process")
            return False
            
        all_data = []
        
        for input_file in input_files:
            file_path = os.path.join(self.input_directory, input_file)
            self.statistics['processed_files'] += 1
            
            try:
                # Load data
                data = self._load_data(file_path)
                if not data:
                    self.statistics['failed_files'] += 1
                    continue
                    
                # Process data
                processed_data = self._transform_data(data)
                
                # Validate data
                valid_data, invalid_count = self._validate_data(processed_data)
                
                self.statistics['total_records'] += len(processed_data)
                self.statistics['valid_records'] += len(valid_data)
                self.statistics['invalid_records'] += invalid_count
                
                # Add to all data
                all_data.extend(valid_data)
                
                self.statistics['successful_files'] += 1
            except Exception as e:
                self.logger.error(f"Error processing file {input_file}: {str(e)}")
                self.statistics['failed_files'] += 1
        
        # Export data
        if all_data:
            output_file = f"processed_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
            output_path = os.path.join(self.output_directory, output_file)
            
            if output_format in self.exporters:
                try:
                    self.exporters[output_format](all_data, output_path)
                    self.logger.info(f"Data exported to {output_path}")
                except Exception as e:
                    self.logger.error(f"Error exporting data: {str(e)}")
                    self.last_error = f"Export error: {str(e)}"
                    return False
            else:
                self.logger.error(f"Unsupported output format: {output_format}")
                return False
        
        # Update statistics
        self.statistics['processing_time'] = time.time() - start_time
        self.statistics['last_run'] = datetime.datetime.now().isoformat()
        
        return True
    
    def _load_data(self, file_path):
        # Check cache first
        if file_path in self.data_cache:
            cache_entry = self.data_cache[file_path]
            if time.time() - cache_entry['timestamp'] < self.cache_expiry:
                self.logger.info(f"Using cached data for {file_path}")
                return cache_entry['data']
        
        # Load data based on file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower().strip('.')
        
        try:
            if ext == 'csv':
                data = self._load_csv(file_path)
            elif ext == 'json':
                data = self._load_json(file_path)
            else:
                self.logger.error(f"Unsupported file format: {ext}")
                return None
                
            # Cache data
            if len(self.data_cache) >= self.max_cache_size:
                # Remove oldest cache entry
                oldest = min(self.data_cache.items(), key=lambda x: x[1]['timestamp'])
                del self.data_cache[oldest[0]]
                
            self.data_cache[file_path] = {
                'data': data,
                'timestamp': time.time()
            }
            
            return data
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {str(e)}")
            return None
    
    def _load_csv(self, file_path):
        # Load data from CSV file
        data = []
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data
    
    def _load_json(self, file_path):
        # Load data from JSON file
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _transform_data(self, data):
        # Apply transformations based on configuration
        transformed_data = []
        
        for item in data:
            transformed_item = {}
            
            for field, value in item.items():
                # Only include allowed fields if specified
                if self.allowed_fields and field not in self.allowed_fields:
                    continue
                    
                # Apply transformations based on field type
                if field in self.field_types:
                    field_type = self.field_types[field]
                    if field_type == 'string':
                        # Apply string transformations
                        value = self.transformers['trim'](value)
                    elif field_type == 'number':
                        # Try to convert to number
                        try:
                            value = float(value) if '.' in str(value) else int(value)
                        except (ValueError, TypeError):
                            self.logger.warning(f"Could not convert '{value}' to number")
                    elif field_type == 'date':
                        # No transformation for dates in this example
                        pass
                
                transformed_item[field] = value
            
            transformed_data.append(transformed_item)
        
        return transformed_data
    
    def _validate_data(self, data):
        # Validate data based on rules
        valid_data = []
        invalid_count = 0
        
        for item in data:
            is_valid = True
            
            # Check required fields
            for field in self.required_fields:
                if field not in item or not self.validators['not_empty'](item[field]):
                    is_valid = False
                    self.logger.warning(f"Missing required field: {field}")
                    break
            
            # Check field types
            for field, field_type in self.field_types.items():
                if field in item:
                    if field_type == 'number' and not self.validators['is_numeric'](item[field]):
                        is_valid = False
                        self.logger.warning(f"Invalid number: {item[field]}")
                    elif field_type == 'date' and not self.validators['is_date'](item[field]):
                        is_valid = False
                        self.logger.warning(f"Invalid date: {item[field]}")
            
            if is_valid:
                valid_data.append(item)
            else:
                invalid_count += 1
        
        return valid_data, invalid_count
    
    def _export_csv(self, data, output_path):
        # Export data to CSV
        if not data:
            return
            
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    def _export_json(self, data, output_path):
        # Export data to JSON
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_statistics(self):
        # Return current statistics
        return self.statistics
    
    def clear_cache(self):
        # Clear the data cache
        self.data_cache = {}
        self.logger.info("Cache cleared")
        return True
    
    def register_transformer(self, name, transformer_func):
        # Register a custom transformer
        if not callable(transformer_func):
            raise ValueError("Transformer must be callable")
        self.transformers[name] = transformer_func
        self.logger.info(f"Transformer registered: {name}")
        return True
    
    def register_validator(self, name, validator_func):
        # Register a custom validator
        if not callable(validator_func):
            raise ValueError("Validator must be callable")
        self.validators[name] = validator_func
        self.logger.info(f"Validator registered: {name}")
        return True
    
    def register_exporter(self, format_name, exporter_func):
        # Register a custom exporter
        if not callable(exporter_func):
            raise ValueError("Exporter must be callable")
        self.exporters[format_name] = exporter_func
        self.logger.info(f"Exporter registered: {format_name}")
        return True
    
    def generate_report(self, report_format="text"):
        # Generate a report of processing statistics
        if report_format == "text":
            report = f"Data Processing Report\n"
            report += f"===================\n\n"
            report += f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"Last Run: {self.statistics.get('last_run', 'Never')}\n\n"
            report += f"Files:\n"
            report += f"  Processed: {self.statistics.get('processed_files', 0)}\n"
            report += f"  Successful: {self.statistics.get('successful_files', 0)}\n"
            report += f"  Failed: {self.statistics.get('failed_files', 0)}\n\n"
            report += f"Records:\n"
            report += f"  Total: {self.statistics.get('total_records', 0)}\n"
            report += f"  Valid: {self.statistics.get('valid_records', 0)}\n"
            report += f"  Invalid: {self.statistics.get('invalid_records', 0)}\n\n"
            report += f"Performance:\n"
            report += f"  Processing Time: {self.statistics.get('processing_time', 0):.2f} seconds\n"
            
            return report
        elif report_format == "json":
            return json.dumps(self.statistics, indent=2)
        else:
            self.logger.error(f"Unsupported report format: {report_format}")
            return None
    
    def validate_directory_structure(self):
        # Validate and create directory structure
        # This method does too much and should be split
        
        # Check input directory
        if not os.path.exists(self.input_directory):
            try:
                os.makedirs(self.input_directory)
                self.logger.info(f"Created input directory: {self.input_directory}")
            except Exception as e:
                self.logger.error(f"Could not create input directory: {str(e)}")
                return False
        elif not os.path.isdir(self.input_directory):
            self.logger.error(f"Input path is not a directory: {self.input_directory}")
            return False
        
        # Check output directory
        if not os.path.exists(self.output_directory):
            try:
                os.makedirs(self.output_directory)
                self.logger.info(f"Created output directory: {self.output_directory}")
            except Exception as e:
                self.logger.error(f"Could not create output directory: {str(e)}")
                return False
        elif not os.path.isdir(self.output_directory):
            self.logger.error(f"Output path is not a directory: {self.output_directory}")
            return False
        
        # Create sample configuration if it doesn't exist
        if not self.config_file:
            self.config_file = os.path.join(self.output_directory, "config.json")
            
        if not os.path.exists(self.config_file):
            try:
                sample_config = {
                    "allowed_fields": ["id", "name", "email", "age", "date"],
                    "required_fields": ["id", "name"],
                    "field_types": {
                        "id": "string",
                        "name": "string",
                        "email": "string",
                        "age": "number",
                        "date": "date"
                    },
                    "max_cache_size": 100,
                    "cache_expiry": 3600
                }
                
                with open(self.config_file, 'w') as f:
                    json.dump(sample_config, f, indent=2)
                    
                self.logger.info(f"Created sample configuration: {self.config_file}")
            except Exception as e:
                self.logger.error(f"Could not create sample configuration: {str(e)}")
                
        return True
    
    def generate_sample_data(self, num_records=100, output_file=None):
        # Generate sample data for testing
        # This method is too long and does too much
        
        if not output_file:
            output_file = os.path.join(self.input_directory, f"sample_data_{int(time.time())}.json")
            
        # Define data generation parameters
        domains = ["example.com", "test.com", "sample.org", "demo.net"]
        name_parts = ["John", "Jane", "Bob", "Alice", "Charlie", "David", "Emma", "Frank", "Grace", "Helen"]
        
        data = []
        
        for i in range(num_records):
            # Generate a random person
            first_name = random.choice(name_parts)
            last_name = random.choice(name_parts)
            name = f"{first_name} {last_name}"
            
            # Generate email
            email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
            
            # Generate age
            age = random.randint(18, 80)
            
            # Generate date
            year = random.randint(2000, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Simplify to avoid month/day validation
            date = f"{year:04d}-{month:02d}-{day:02d}"
            
            # Generate record
            record = {
                "id": f"ID-{i+1:06d}",
                "name": name,
                "email": email,
                "age": age,
                "date": date,
                "active": random.choice([True, False]),
                "notes": ''.join(random.choices(string.ascii_letters + ' ' * 10, k=random.randint(10, 50)))
            }
            
            data.append(record)
        
        # Write data to file
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.info(f"Generated sample data: {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"Error generating sample data: {str(e)}")
            return None
