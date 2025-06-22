import os
import sys

import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar o app workflow já existente em vez de recriar a lógica
from src.agents.workflow_agent import supervisor as workflow_app

# Configuração da página Streamlit
st.set_page_config(
    page_title="Multi-Agent Smell Detector", page_icon="🔍", layout="wide"
)


def execute_workflow(user_code):
    """Executa o workflow com o código fornecido pelo usuário"""
    response = workflow_app.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_code,
                }
            ]
        }
    )
    return response


def extract_supervisor_response(response):
    """Extrai a resposta do supervisor do objeto de resposta completo"""
    if not isinstance(response, dict):
        return str(response)

    # Se a resposta contém uma chave 'messages'
    if "messages" in response:
        messages = response["messages"]

        # Procura pela última mensagem AIMessage com nome 'supervisor'
        for message in reversed(messages):
            try:
                if (
                    hasattr(message, "name")
                    and message.name == "supervisor"
                    and hasattr(message, "content")
                ):
                    return message.content
            except AttributeError:
                # Tenta acessar como dicionário se falhar como objeto
                if (
                    isinstance(message, dict)
                    and message.get("name") == "supervisor"
                    and "content" in message
                ):
                    return message["content"]

        # Caso não encontre uma mensagem específica do supervisor, pega a última AIMessage
        for message in reversed(messages):
            try:
                if hasattr(message, "content"):
                    return message.content
            except AttributeError:
                if isinstance(message, dict) and "content" in message:
                    return message["content"]

    # Fallback para o caso da estrutura ser diferente
    return str(response)


def display_all_messages(response):
    """Exibe todas as mensagens do fluxo de comunicação"""
    if "messages" in response:
        messages = response["messages"]
        messages_data = []

        for i, message in enumerate(messages):
            try:
                role = message.name if hasattr(message, "name") else (
                    message.get("name") if isinstance(message, dict) else "unknown"
                )

                content = message.content if hasattr(message, "content") else (
                    message.get("content") if isinstance(message, dict) else str(message)
                )

                messages_data.append(
                    {
                        "Ordem": i + 1,
                        "Agente": role,
                        "Conteúdo": content[:100] + "..." if len(str(content)) > 100 else content,
                    }
                )
            except Exception as e:
                messages_data.append(
                    {
                        "Ordem": i + 1,
                        "Agente": "Erro",
                        "Conteúdo": f"Erro ao processar mensagem: {str(e)}",
                    }
                )

        # Criar DataFrame para exibição
        df = pd.DataFrame(messages_data)
        st.dataframe(df)

        # Exibir conteúdo completo de cada mensagem em expanders
        for i, message in enumerate(messages):
            try:
                role = message.name if hasattr(message, "name") else (
                    message.get("name") if isinstance(message, dict) else "unknown"
                )

                content = message.content if hasattr(message, "content") else (
                    message.get("content") if isinstance(message, dict) else str(message)
                )

                with st.expander(f"Mensagem {i+1}: {role}"):
                    st.markdown(content)
            except Exception as e:
                with st.expander(f"Mensagem {i+1}: Erro"):
                    st.error(f"Erro ao processar mensagem: {str(e)}")
    else:
        st.warning("Nenhuma mensagem encontrada na resposta.")


def main():
    """Função principal da aplicação Streamlit"""

    st.title("🔍 Multi-Agent Smell Detector")
    st.markdown(
        """
    Esta ferramenta analisa código Python em busca de:
    - Code smells (classes God, métodos longos, etc.)
    - Vulnerabilidades de segurança
    """
    )

    with st.expander("ℹ️ Sobre esta ferramenta", expanded=False):
        st.markdown(
            """
        **Multi-Agent Smell Detector** utiliza agentes de IA para analisar código Python e identificar:
        
        - **Code Smells**: Problemas estruturais que afetam a manutenibilidade
        - **Vulnerabilidades de Segurança**: Riscos como injeção SQL e outras falhas
        
        Os agentes trabalham em conjunto para fornecer uma análise completa e sugestões de melhoria.
        """
        )

    st.subheader("📝 Insira o código para análise")
    user_code = st.text_area(
        "Código Python",
        value="",
        height=400,
        placeholder="Cole seu código Python aqui...",
    )

    # Botão para executar a análise
    if st.button("🔍 Analisar Código", type="primary"):
        if not user_code.strip():
            st.warning("Por favor, insira algum código para análise.")
            return

        with st.spinner("Analisando o código..."):
            try:
                # Executar o workflow com o código fornecido
                response = execute_workflow(user_code)

                # Extrair e exibir a resposta do supervisor
                st.subheader("📊 Resultado da Análise")
                supervisor_response = extract_supervisor_response(response)
                st.markdown(supervisor_response)

                # Exibir todas as mensagens em modo debug expandível
                with st.expander("🔍 Detalhes da Conversa (Debug)", expanded=False):
                    st.subheader("Histórico de mensagens entre os agentes")
                    display_all_messages(response)

                    st.subheader("Resposta completa (JSON)")
                    st.json(response)

            except Exception as e:
                st.error(f"Ocorreu um erro ao analisar o código: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()
