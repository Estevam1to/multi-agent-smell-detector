"""
Casos de teste com exemplos de code smells para validação.

Cada exemplo contém código com um smell específico e metadados sobre o smell esperado.
"""

# 1. Long Method (> 67 linhas)
LONG_METHOD_EXAMPLE = {
    "code": '''
def process_user_data(user_id):
    """Método muito longo que viola o princípio de responsabilidade única."""
    # Buscar usuário
    user = database.get_user(user_id)
    if not user:
        raise ValueError("User not found")

    # Validar dados
    if not user.email:
        raise ValueError("Email is required")
    if not user.name:
        raise ValueError("Name is required")
    if not user.age or user.age < 0:
        raise ValueError("Invalid age")

    # Processar email
    email_parts = user.email.split("@")
    if len(email_parts) != 2:
        raise ValueError("Invalid email")
    domain = email_parts[1]

    # Validar domínio
    if domain not in ALLOWED_DOMAINS:
        raise ValueError("Domain not allowed")

    # Processar nome
    name_parts = user.name.split(" ")
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    # Calcular categoria de idade
    if user.age < 18:
        age_category = "minor"
    elif user.age < 30:
        age_category = "young_adult"
    elif user.age < 60:
        age_category = "adult"
    else:
        age_category = "senior"

    # Processar preferências
    preferences = {}
    if user.preferences:
        for pref in user.preferences:
            if pref.type == "email":
                preferences["email_frequency"] = pref.value
            elif pref.type == "notifications":
                preferences["notifications_enabled"] = pref.value
            elif pref.type == "theme":
                preferences["theme"] = pref.value

    # Calcular score
    score = 0
    if user.is_active:
        score += 10
    if user.email_verified:
        score += 20
    if user.phone_verified:
        score += 15
    if len(user.purchases) > 0:
        score += 5 * len(user.purchases)

    # Atualizar banco de dados
    user.first_name = first_name
    user.last_name = last_name
    user.age_category = age_category
    user.preferences = preferences
    user.score = score
    user.last_updated = datetime.now()

    database.save(user)

    # Enviar notificações
    if preferences.get("notifications_enabled"):
        send_notification(user, "Profile updated")

    return user
''',
    "smell_type": "long_method",
    "expected_detection": True,
    "line_count": 70,
}

# 2. Long Parameter List (> 4 parâmetros)
LONG_PARAMETER_LIST_EXAMPLE = {
    "code": '''
def create_user(first_name, last_name, email, phone, address, city, state, country, postal_code):
    """Função com muitos parâmetros."""
    return User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code
    )
''',
    "smell_type": "long_parameter_list",
    "expected_detection": True,
    "parameter_count": 9,
}

# 3. Long Statement (> 80 caracteres)
LONG_STATEMENT_EXAMPLE = {
    "code": '''
def calculate_total():
    result = some_very_long_function_name(parameter1, parameter2, parameter3) if condition1 and condition2 else another_long_function(param4, param5)
    return result
''',
    "smell_type": "long_statement",
    "expected_detection": True,
    "line_length": 155,
}

# 4. Long Identifier (> 20 caracteres)
LONG_IDENTIFIER_EXAMPLE = {
    "code": '''
def calculate_total_price_with_discount_and_taxes_for_premium_customer(price):
    """Identificador muito longo."""
    return price * 1.1

very_long_variable_name_that_describes_everything_in_detail = 42
''',
    "smell_type": "long_identifier",
    "expected_detection": True,
    "identifier_length": 66,
}

# 5. Empty Catch Block
EMPTY_CATCH_BLOCK_EXAMPLE = {
    "code": '''
def risky_operation():
    try:
        dangerous_code()
    except Exception:
        pass  # Silencia todos os erros!
''',
    "smell_type": "empty_catch_block",
    "expected_detection": True,
}

# 6. Complex Method (CC > 7)
COMPLEX_METHOD_EXAMPLE = {
    "code": '''
def complex_logic(data):
    """Método com alta complexidade ciclomática."""
    if data:
        if data.valid:
            if data.type == "A":
                if data.status == "active":
                    for item in data.items:
                        if item.checked:
                            if item.value > 0:
                                if item.priority == "high":
                                    return True
    return False
''',
    "smell_type": "complex_method",
    "expected_detection": True,
    "cyclomatic_complexity": 8,
}

# 7. Complex Conditional (> 2 operadores lógicos)
COMPLEX_CONDITIONAL_EXAMPLE = {
    "code": '''
def check_eligibility(user):
    if user.age > 18 and user.country == "BR" and user.verified and user.balance > 100 and user.active:
        return True
    return False
''',
    "smell_type": "complex_conditional",
    "expected_detection": True,
    "logical_operators_count": 4,
}

# 8. Missing Default (match-case sem default)
MISSING_DEFAULT_EXAMPLE = {
    "code": '''
def process_status(status):
    match status:
        case "active":
            return "Processing active"
        case "inactive":
            return "Processing inactive"
    # Falta case _: para casos não previstos
''',
    "smell_type": "missing_default",
    "expected_detection": True,
}

# 9. Long Lambda Function (> 80 caracteres)
LONG_LAMBDA_FUNCTION_EXAMPLE = {
    "code": '''
transform = lambda x: x * 2 if x > 0 else x * -1 if x < 0 else 0 if x == 0 else None
numbers = [1, -2, 3, -4]
result = map(transform, numbers)
''',
    "smell_type": "long_lambda_function",
    "expected_detection": True,
    "lambda_length": 84,
}

# 10. Long Message Chain (> 2 métodos encadeados)
LONG_MESSAGE_CHAIN_EXAMPLE = {
    "code": '''
def get_zip_code(customer):
    return customer.get_address().get_city().get_zip_code().validate()
''',
    "smell_type": "long_message_chain",
    "expected_detection": True,
    "chain_length": 4,
}

# 11. Magic Number
MAGIC_NUMBER_EXAMPLE = {
    "code": '''
def calculate_gravity(mass, height):
    return mass * 9.81 * height  # O que é 9.81?

def calculate_discount(price):
    if price > 1000:
        return price * 0.85  # 15% desconto
    return price
''',
    "smell_type": "magic_number",
    "expected_detection": True,
    "magic_numbers": [9.81, 0.85, 1000],
}

# Código limpo (sem code smells) para teste de falso positivo
CLEAN_CODE_EXAMPLE = {
    "code": '''
def calculate_total(items):
    """Função simples e limpa."""
    return sum(item.price for item in items)

def validate_email(email):
    """Valida formato de email."""
    if "@" not in email:
        return False
    return True
''',
    "smell_type": "none",
    "expected_detection": False,
}

# Lista de todos os exemplos
ALL_EXAMPLES = [
    LONG_METHOD_EXAMPLE,
    LONG_PARAMETER_LIST_EXAMPLE,
    LONG_STATEMENT_EXAMPLE,
    LONG_IDENTIFIER_EXAMPLE,
    EMPTY_CATCH_BLOCK_EXAMPLE,
    COMPLEX_METHOD_EXAMPLE,
    COMPLEX_CONDITIONAL_EXAMPLE,
    MISSING_DEFAULT_EXAMPLE,
    LONG_LAMBDA_FUNCTION_EXAMPLE,
    LONG_MESSAGE_CHAIN_EXAMPLE,
    MAGIC_NUMBER_EXAMPLE,
    CLEAN_CODE_EXAMPLE,
]
