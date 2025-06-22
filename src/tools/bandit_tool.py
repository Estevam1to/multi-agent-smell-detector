import json
import subprocess
import tempfile
from pathlib import Path


def run_bandit_tool(code: str) -> list:
    """
    Runs Bandit on Python code and returns the formatted results.
    Fixes the 'CalledProcessError' issue when vulnerabilities are found.

    Args:
        code (str): Python code to be analyzed.

    Returns:
        List[Dict]: List of found vulnerabilities (empty if none).
    """
    print("Running Bandit tool on the provided code...")
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
