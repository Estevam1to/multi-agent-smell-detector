"""
Script de exemplo para testar o formato DPy de saída.

Demonstra como usar a API com output_format="dpy" para obter
resultados compatíveis com a ferramenta DPy.
"""

import requests
import json

# Código de exemplo com code smells
EXAMPLE_CODE = '''
def validate_eligibility(user, age, country, verified, balance):
    """Função com múltiplos code smells para teste."""
    # Complex conditional (4 operadores)
    if user.age > 18 and user.country == "BR" and user.verified and user.balance > 100 and user.active:
        return process_complex_data(user)
    return False

def process_complex_data(data):
    """Complex Method com alta complexidade ciclomática."""
    if data:
        if data.valid:
            if data.type == "A":
                if data.status == "active":
                    for item in data.items:
                        if item.checked:
                            if item.value > 0:
                                if item.priority == "high":
                                    return calculate_result_with_magic_number(item)
    return False

def calculate_result_with_magic_number(item):
    """Função com magic number."""
    return item.value * 9.81 * 0.85  # Magic numbers!

def create_user(first_name, last_name, email, phone, address, city, state, country, postal_code):
    """Long parameter list - 9 parâmetros."""
    return f"{first_name} {last_name}"
'''

def test_default_format():
    """Testa o formato padrão (original)."""
    print("=" * 80)
    print("TESTE: FORMATO PADRÃO (DEFAULT)")
    print("=" * 80)

    response = requests.post(
        "http://localhost:8000/api/analyze",
        json={
            "python_code": EXAMPLE_CODE,
            "file_path": "/home/luis-chaves/Downloads/dataset/files/Code/validate.py",
            "output_format": "default"
        }
    )

    if response.status_code == 200:
        result = response.json()
        print(f"\nTotal de smells detectados: {result['total_smells_detected']}")
        print(f"Agentes executados: {result['agents_executed']}")
        print(f"Formato: {result['output_format']}")
        print("\nCode Smells detectados:")
        print(json.dumps(result['code_smells'], indent=2, ensure_ascii=False))
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)


def test_dpy_format():
    """Testa o formato DPy (compatível com ferramenta DPy)."""
    print("\n" + "=" * 80)
    print("TESTE: FORMATO DPy")
    print("=" * 80)

    response = requests.post(
        "http://localhost:8000/api/analyze",
        json={
            "python_code": EXAMPLE_CODE,
            "file_path": "/home/luis-chaves/Downloads/dataset/files/Code/validate.py",
            "output_format": "dpy",
            "project_name": "Code"
        }
    )

    if response.status_code == 200:
        result = response.json()
        print(f"\nTotal de smells detectados: {result['total_smells_detected']}")
        print(f"Agentes executados: {result['agents_executed']}")
        print(f"Formato: {result['output_format']}")
        print("\nCode Smells no formato DPy:")
        print(json.dumps(result['code_smells'], indent=2, ensure_ascii=False))
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)


def compare_formats():
    """Compara os dois formatos lado a lado."""
    print("\n" + "=" * 80)
    print("COMPARAÇÃO DE FORMATOS")
    print("=" * 80)

    # Formato padrão
    response_default = requests.post(
        "http://localhost:8000/api/analyze",
        json={
            "python_code": EXAMPLE_CODE,
            "output_format": "default"
        }
    )

    # Formato DPy
    response_dpy = requests.post(
        "http://localhost:8000/api/analyze",
        json={
            "python_code": EXAMPLE_CODE,
            "file_path": "/test/validate.py",
            "output_format": "dpy",
            "project_name": "TestProject"
        }
    )

    if response_default.status_code == 200 and response_dpy.status_code == 200:
        default = response_default.json()
        dpy = response_dpy.json()

        print("\nESTRUTURA DO FORMATO PADRÃO:")
        if default['code_smells']:
            print(json.dumps(default['code_smells'][0], indent=2, ensure_ascii=False))

        print("\nESTRUTURA DO FORMATO DPy:")
        if dpy['code_smells']:
            print(json.dumps(dpy['code_smells'][0], indent=2, ensure_ascii=False))
    else:
        print("Erro ao executar comparação")


if __name__ == "__main__":
    print("Testando API com diferentes formatos de saída\n")
    print("Certifique-se de que o servidor está rodando em http://localhost:8000")
    print()

    try:
        # Testa formato padrão
        test_default_format()

        # Testa formato DPy
        test_dpy_format()

        # Compara formatos
        compare_formats()

        print("\n" + "=" * 80)
        print("TESTES CONCLUÍDOS!")
        print("=" * 80)

    except requests.exceptions.ConnectionError:
        print("\nERRO: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor está rodando:")
        print("  python src/app.py")
