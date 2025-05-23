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
        print(f"Error decoding JSON from Bandit. STDERR: {result.stderr}")
        return []
    finally:
        Path(temp_file_path).unlink(missing_ok=True)


def write_python_file(code: str) -> str:
    """
    Writes Python code to a temporary file and returns the file path.

    Args:
        code (str): Python code to be written.

    Returns:
        None: saves the code to a file.
    """
    with open("temp_code.py", "w") as temp_file:
        temp_file.write(code)


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

response = security_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": """
import datetime
import math
import os
import csv

class ReportGenerator:
    Class responsible for generating various types of reports with sales data.
    This class has lots of duplicate code and methods with too many parameters.

    
    def __init__(self, company_name, report_directory, logo_path, company_address, 
                 company_phone, company_email, tax_id, report_footer, include_header=True,
                 include_footer=True, include_timestamps=True, report_prefix="Report",
                 default_currency="USD", decimal_places=2, date_format="%Y-%m-%d"):
        # Too many parameters in constructor (code smell)
        self.company_name = company_name
        self.report_directory = report_directory
        self.logo_path = logo_path
        self.company_address = company_address
        self.company_phone = company_phone
        self.company_email = company_email
        self.tax_id = tax_id
        self.report_footer = report_footer
        self.include_header = include_header
        self.include_footer = include_footer
        self.include_timestamps = include_timestamps
        self.report_prefix = report_prefix
        self.default_currency = default_currency
        self.decimal_places = decimal_places
        self.date_format = date_format
        
        # Create report directory if it doesn't exist
        if not os.path.exists(self.report_directory):
            os.makedirs(self.report_directory)
    
    def generate_daily_sales_report(self, sales_data, report_date, store_id=None, 
                                   department=None, include_tax=True, include_discounts=True,
                                   include_returns=True, format_type="csv"):
        # Method with too many parameters (code smell)
        if not sales_data:
            print("No sales data provided")
            return None
            
        # Filter data for the specific date
        date_str = report_date.strftime(self.date_format)
        filtered_data = [sale for sale in sales_data 
                        if sale.get("date") == date_str and
                        (store_id is None or sale.get("store_id") == store_id) and
                        (department is None or sale.get("department") == department)]
        
        if not filtered_data:
            print(f"No sales data for date {date_str}")
            return None
            
        # Prepare report filename
        filename = f"{self.report_prefix}_Daily_Sales_{date_str}"
        if store_id:
            filename += f"_Store{store_id}"
        if department:
            filename += f"_{department}"
        filename += f".{format_type}"
        
        report_path = os.path.join(self.report_directory, filename)
        
        # Calculate totals
        total_sales = sum(sale.get("amount", 0) for sale in filtered_data)
        total_items = sum(sale.get("quantity", 0) for sale in filtered_data)
        
        if include_tax:
            total_tax = sum(sale.get("tax", 0) for sale in filtered_data)
        else:
            total_tax = 0
            
        if include_discounts:
            total_discounts = sum(sale.get("discount", 0) for sale in filtered_data)
        else:
            total_discounts = 0
            
        if include_returns:
            returns_data = [sale for sale in filtered_data if sale.get("type") == "return"]
            total_returns = sum(sale.get("amount", 0) for sale in returns_data)
        else:
            total_returns = 0
            
        net_sales = total_sales - total_returns - total_discounts + total_tax
        
        # Write report
        if format_type == "csv":
            self._write_csv_report(report_path, filtered_data, {
                "Date": date_str,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Total Discounts": self._format_currency(total_discounts) if include_discounts else "N/A",
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Net Sales": self._format_currency(net_sales)
            })
        elif format_type == "txt":
            self._write_txt_report(report_path, filtered_data, {
                "Date": date_str,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Total Discounts": self._format_currency(total_discounts) if include_discounts else "N/A",
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Net Sales": self._format_currency(net_sales)
            })
        else:
            print(f"Unsupported report format: {format_type}")
            return None
            
        print(f"Daily sales report generated: {report_path}")
        return report_path
    
    def generate_monthly_sales_report(self, sales_data, year, month, store_id=None, 
                                     department=None, include_tax=True, include_discounts=True,
                                     include_returns=True, format_type="csv"):
        # Duplicate code with daily report - should be refactored (code smell)
        if not sales_data:
            print("No sales data provided")
            return None
            
        # Filter data for the specific month
        filtered_data = []
        for sale in sales_data:
            sale_date = datetime.datetime.strptime(sale.get("date"), self.date_format)
            if (sale_date.year == year and sale_date.month == month and
                (store_id is None or sale.get("store_id") == store_id) and
                (department is None or sale.get("department") == department)):
                filtered_data.append(sale)
        
        if not filtered_data:
            print(f"No sales data for {year}-{month}")
            return None
            
        # Prepare report filename
        month_name = datetime.date(year, month, 1).strftime("%B")
        filename = f"{self.report_prefix}_Monthly_Sales_{year}_{month_name}"
        if store_id:
            filename += f"_Store{store_id}"
        if department:
            filename += f"_{department}"
        filename += f".{format_type}"
        
        report_path = os.path.join(self.report_directory, filename)
        
        # Calculate totals - duplicate code from daily report (code smell)
        total_sales = sum(sale.get("amount", 0) for sale in filtered_data)
        total_items = sum(sale.get("quantity", 0) for sale in filtered_data)
        
        if include_tax:
            total_tax = sum(sale.get("tax", 0) for sale in filtered_data)
        else:
            total_tax = 0
            
        if include_discounts:
            total_discounts = sum(sale.get("discount", 0) for sale in filtered_data)
        else:
            total_discounts = 0
            
        if include_returns:
            returns_data = [sale for sale in filtered_data if sale.get("type") == "return"]
            total_returns = sum(sale.get("amount", 0) for sale in returns_data)
        else:
            total_returns = 0
            
        net_sales = total_sales - total_returns - total_discounts + total_tax
        
        # Daily breakdown
        daily_sales = {}
        for sale in filtered_data:
            day = datetime.datetime.strptime(sale.get("date"), self.date_format).day
            if day not in daily_sales:
                daily_sales[day] = 0
            daily_sales[day] += sale.get("amount", 0)
        
        # Write report
        if format_type == "csv":
            self._write_csv_report(report_path, filtered_data, {
                "Year": year,
                "Month": month_name,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Total Discounts": self._format_currency(total_discounts) if include_discounts else "N/A",
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Net Sales": self._format_currency(net_sales),
                "Daily Breakdown": daily_sales
            })
        elif format_type == "txt":
            self._write_txt_report(report_path, filtered_data, {
                "Year": year,
                "Month": month_name,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Total Discounts": self._format_currency(total_discounts) if include_discounts else "N/A",
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Net Sales": self._format_currency(net_sales),
                "Daily Breakdown": daily_sales
            })
        else:
            print(f"Unsupported report format: {format_type}")
            return None
            
        print(f"Monthly sales report generated: {report_path}")
        return report_path
    
    def generate_product_sales_report(self, sales_data, start_date, end_date, 
                                     product_id=None, store_id=None, department=None,
                                     include_tax=True, min_quantity=0, format_type="csv"):
        # Another method with too many parameters and duplicate code (code smell)
        if not sales_data:
            print("No sales data provided")
            return None
            
        # Convert dates to datetime objects
        start_datetime = datetime.datetime.strptime(start_date, self.date_format)
        end_datetime = datetime.datetime.strptime(end_date, self.date_format)
            
        # Filter data for the date range and product
        filtered_data = []
        for sale in sales_data:
            sale_date = datetime.datetime.strptime(sale.get("date"), self.date_format)
            if (start_datetime <= sale_date <= end_datetime and
                (product_id is None or sale.get("product_id") == product_id) and
                (store_id is None or sale.get("store_id") == store_id) and
                (department is None or sale.get("department") == department) and
                sale.get("quantity", 0) >= min_quantity):
                filtered_data.append(sale)
        
        if not filtered_data:
            print(f"No product sales data for the specified criteria")
            return None
            
        # Prepare report filename
        filename = f"{self.report_prefix}_Product_Sales_{start_date}_to_{end_date}"
        if product_id:
            filename += f"_Product{product_id}"
        if store_id:
            filename += f"_Store{store_id}"
        if department:
            filename += f"_{department}"
        filename += f".{format_type}"
        
        report_path = os.path.join(self.report_directory, filename)
        
        # Calculate totals - more duplicate code (code smell)
        total_sales = sum(sale.get("amount", 0) for sale in filtered_data)
        total_items = sum(sale.get("quantity", 0) for sale in filtered_data)
        
        if include_tax:
            total_tax = sum(sale.get("tax", 0) for sale in filtered_data)
        else:
            total_tax = 0
            
        # Group by product
        product_sales = {}
        for sale in filtered_data:
            prod_id = sale.get("product_id")
            if prod_id not in product_sales:
                product_sales[prod_id] = {
                    "quantity": 0,
                    "amount": 0,
                    "tax": 0
                }
            product_sales[prod_id]["quantity"] += sale.get("quantity", 0)
            product_sales[prod_id]["amount"] += sale.get("amount", 0)
            product_sales[prod_id]["tax"] += sale.get("tax", 0)
        
        # Write report
        if format_type == "csv":
            self._write_csv_report(report_path, filtered_data, {
                "Start Date": start_date,
                "End Date": end_date,
                "Product ID": product_id,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Product Breakdown": product_sales
            })
        elif format_type == "txt":
            self._write_txt_report(report_path, filtered_data, {
                "Start Date": start_date,
                "End Date": end_date,
                "Product ID": product_id,
                "Store ID": store_id,
                "Department": department,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Tax": self._format_currency(total_tax) if include_tax else "N/A",
                "Product Breakdown": product_sales
            })
        else:
            print(f"Unsupported report format: {format_type}")
            return None
            
        print(f"Product sales report generated: {report_path}")
        return report_path
    
    def generate_employee_performance_report(self, sales_data, employee_data, start_date, end_date,
                                           employee_id=None, department=None, store_id=None,
                                           include_commission=True, include_returns=True, format_type="csv"):
        # Yet another method with too many parameters and duplicate code (code smell)
        if not sales_data or not employee_data:
            print("No data provided")
            return None
            
        # Convert dates to datetime objects
        start_datetime = datetime.datetime.strptime(start_date, self.date_format)
        end_datetime = datetime.datetime.strptime(end_date, self.date_format)
            
        # Filter data for the date range and employee
        filtered_data = []
        for sale in sales_data:
            sale_date = datetime.datetime.strptime(sale.get("date"), self.date_format)
            if (start_datetime <= sale_date <= end_datetime and
                (employee_id is None or sale.get("employee_id") == employee_id) and
                (store_id is None or sale.get("store_id") == store_id) and
                (department is None or sale.get("department") == department)):
                filtered_data.append(sale)
        
        if not filtered_data:
            print(f"No sales data for the specified criteria")
            return None
            
        # Prepare report filename
        filename = f"{self.report_prefix}_Employee_Performance_{start_date}_to_{end_date}"
        if employee_id:
            filename += f"_Employee{employee_id}"
        if department:
            filename += f"_{department}"
        if store_id:
            filename += f"_Store{store_id}"
        filename += f".{format_type}"
        
        report_path = os.path.join(self.report_directory, filename)
        
        # Calculate employee performances
        employee_performance = {}
        for sale in filtered_data:
            emp_id = sale.get("employee_id")
            if emp_id not in employee_performance:
                employee_performance[emp_id] = {
                    "sales_count": 0,
                    "total_amount": 0,
                    "total_items": 0,
                    "returns_count": 0,
                    "returns_amount": 0,
                    "commission": 0
                }
                
                # Add employee details
                for emp in employee_data:
                    if emp.get("id") == emp_id:
                        employee_performance[emp_id]["name"] = emp.get("name")
                        employee_performance[emp_id]["department"] = emp.get("department")
                        employee_performance[emp_id]["commission_rate"] = emp.get("commission_rate", 0)
                        break
            
            # Update statistics
            sale_type = sale.get("type", "sale")
            sale_amount = sale.get("amount", 0)
            sale_quantity = sale.get("quantity", 0)
            
            if sale_type == "return" and include_returns:
                employee_performance[emp_id]["returns_count"] += 1
                employee_performance[emp_id]["returns_amount"] += sale_amount
            else:
                employee_performance[emp_id]["sales_count"] += 1
                employee_performance[emp_id]["total_amount"] += sale_amount
                employee_performance[emp_id]["total_items"] += sale_quantity
                
                # Calculate commission
                if include_commission:
                    commission_rate = employee_performance[emp_id].get("commission_rate", 0)
                    commission = sale_amount * commission_rate
                    employee_performance[emp_id]["commission"] += commission
        
        # Calculate totals
        total_sales = sum(emp["total_amount"] for emp in employee_performance.values())
        total_items = sum(emp["total_items"] for emp in employee_performance.values())
        total_returns = sum(emp["returns_amount"] for emp in employee_performance.values()) if include_returns else 0
        total_commission = sum(emp["commission"] for emp in employee_performance.values()) if include_commission else 0
        
        # Write report - duplicate code (code smell)
        if format_type == "csv":
            self._write_csv_report(report_path, filtered_data, {
                "Start Date": start_date,
                "End Date": end_date,
                "Employee ID": employee_id,
                "Department": department,
                "Store ID": store_id,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Total Commission": self._format_currency(total_commission) if include_commission else "N/A",
                "Employee Performance": employee_performance
            })
        elif format_type == "txt":
            self._write_txt_report(report_path, filtered_data, {
                "Start Date": start_date,
                "End Date": end_date,
                "Employee ID": employee_id,
                "Department": department,
                "Store ID": store_id,
                "Total Sales": self._format_currency(total_sales),
                "Total Items": total_items,
                "Total Returns": self._format_currency(total_returns) if include_returns else "N/A",
                "Total Commission": self._format_currency(total_commission) if include_commission else "N/A",
                "Employee Performance": employee_performance
            })
        else:
            print(f"Unsupported report format: {format_type}")
            return None
            
        print(f"Employee performance report generated: {report_path}")
        return report_path
    
    def _format_currency(self, amount):
        # Format a number as currency
        return f"{self.default_currency} {amount:.{self.decimal_places}f}"
    
    def _write_csv_report(self, report_path, data, summary):
        # Write report data to CSV file
        # Method has duplicate code with _write_txt_report (code smell)
        try:
            with open(report_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                if self.include_header:
                    writer.writerow([self.company_name])
                    writer.writerow([self.company_address])
                    writer.writerow([f"Phone: {self.company_phone}, Email: {self.company_email}"])
                    writer.writerow([f"Tax ID: {self.tax_id}"])
                    writer.writerow([])
                
                # Write timestamp
                if self.include_timestamps:
                    writer.writerow([f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                    writer.writerow([])
                
                # Write summary
                writer.writerow(["Report Summary"])
                for key, value in summary.items():
                    if key != "Daily Breakdown" and key != "Product Breakdown" and key != "Employee Performance":
                        writer.writerow([key, value])
                
                writer.writerow([])
                
                # Write detailed data
                writer.writerow([f"Detailed Data ({len(data)} records)"])
                
                if data:
                    # Write column headers based on first record
                    headers = list(data[0].keys())
                    writer.writerow(headers)
                    
                    # Write data rows
                    for row in data:
                        writer.writerow([row.get(header, "") for header in headers])
                
                # Write footer
                if self.include_footer:
                    writer.writerow([])
                    writer.writerow([self.report_footer])
                
            return True
        except Exception as e:
            print(f"Error writing CSV report: {str(e)}")
            return False
    
    def _write_txt_report(self, report_path, data, summary):
        # Write report data to text file
        # Method has duplicate code with _write_csv_report (code smell)
        try:
            with open(report_path, "w") as txtfile:
                # Write header
                if self.include_header:
                    txtfile.write(f"{self.company_name}\n")
                    txtfile.write(f"{self.company_address}\n")
                    txtfile.write(f"Phone: {self.company_phone}, Email: {self.company_email}\n")
                    txtfile.write(f"Tax ID: {self.tax_id}\n")
                    txtfile.write("\n")
                
                # Write timestamp
                if self.include_timestamps:
                    txtfile.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    txtfile.write("\n")
                
                # Write summary
                txtfile.write("Report Summary\n")
                txtfile.write("==============\n")
                for key, value in summary.items():
                    if key != "Daily Breakdown" and key != "Product Breakdown" and key != "Employee Performance":
                        txtfile.write(f"{key}: {value}\n")
                
                # Write special breakdowns if present
                if "Daily Breakdown" in summary:
                    txtfile.write("\nDaily Sales Breakdown\n")
                    txtfile.write("====================\n")
                    for day, amount in sorted(summary["Daily Breakdown"].items()):
                        txtfile.write(f"Day {day}: {self._format_currency(amount)}\n")
                
                if "Product Breakdown" in summary:
                    txtfile.write("\nProduct Sales Breakdown\n")
                    txtfile.write("======================\n")
                    for product_id, stats in summary["Product Breakdown"].items():
                        txtfile.write(f"Product ID: {product_id}\n")
                        txtfile.write(f"  Quantity: {stats['quantity']}\n")
                        txtfile.write(f"  Amount: {self._format_currency(stats['amount'])}\n")
                        txtfile.write(f"  Tax: {self._format_currency(stats['tax'])}\n")
                        txtfile.write("\n")
                
                if "Employee Performance" in summary:
                    txtfile.write("\nEmployee Performance\n")
                    txtfile.write("===================\n")
                    for emp_id, stats in summary["Employee Performance"].items():
                        txtfile.write(f"Employee ID: {emp_id}\n")
                        if "name" in stats:
                            txtfile.write(f"  Name: {stats['name']}\n")
                        if "department" in stats:
                            txtfile.write(f"  Department: {stats['department']}\n")
                        txtfile.write(f"  Sales Count: {stats['sales_count']}\n")
                        txtfile.write(f"  Total Amount: {self._format_currency(stats['total_amount'])}\n")
                        txtfile.write(f"  Total Items: {stats['total_items']}\n")
                        if "returns_count" in stats:
                            txtfile.write(f"  Returns Count: {stats['returns_count']}\n")
                            txtfile.write(f"  Returns Amount: {self._format_currency(stats['returns_amount'])}\n")
                        if "commission" in stats:
                            txtfile.write(f"  Commission: {self._format_currency(stats['commission'])}\n")
                        txtfile.write("\n")
                
                txtfile.write("\n")
                
                # Write detailed data
                txtfile.write(f"Detailed Data ({len(data)} records)\n")
                txtfile.write("==============================\n")
                
                if data:
                    # Write column headers based on first record
                    headers = list(data[0].keys())
                    header_line = " | ".join(headers)
                    txtfile.write(f"{header_line}\n")
                    txtfile.write("-" * len(header_line) + "\n")
                    
                    # Write data rows
                    for row in data:
                        row_values = [str(row.get(header, "")) for header in headers]
                        txtfile.write(" | ".join(row_values) + "\n")
                
                # Write footer
                if self.include_footer:
                    txtfile.write("\n")
                    txtfile.write(f"{self.report_footer}\n")
                
            return True
        except Exception as e:
            print(f"Error writing TXT report: {str(e)}")
            return False
    
    def calculate_statistics(self, data):
        # Calculate various statistics from sales data
        if not data:
            return None
            
        # Extract numerical values
        amounts = [sale.get("amount", 0) for sale in data]
        
        # Calculate statistics
        total = sum(amounts)
        count = len(amounts)
        average = total / count if count > 0 else 0
        minimum = min(amounts) if amounts else 0
        maximum = max(amounts) if amounts else 0
        
        # Calculate median
        sorted_amounts = sorted(amounts)
        mid = len(sorted_amounts) // 2
        median = (sorted_amounts[mid] + sorted_amounts[~mid]) / 2
        
        # Calculate standard deviation
        variance = sum((x - average) ** 2 for x in amounts) / count if count > 0 else 0
        std_dev = math.sqrt(variance)
        
        return {
            "total": total,
            "count": count,
            "average": average,
            "median": median,
            "minimum": minimum,
            "maximum": maximum,
            "range": maximum - minimum,
            "standard_deviation": std_dev
        }

                """,
            }
        ]
    }
)

print(response["messages"][-1].content)
