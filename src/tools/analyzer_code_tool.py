import json
import subprocess
import tempfile
from pathlib import Path


def run_pylint_tool(code: str) -> list:
    """Analyzes the provided Python code for specific code smells using Pylint.
    Returns a structured AnalysisResult object.
    Focuses only on:
    - God Classes (R0902)
    - Long Methods (C0301)
    - Dead Code (W0612)
    """
    print("Running Pylint tool on the provided code...")
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
