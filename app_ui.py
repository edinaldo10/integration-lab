import streamlit as st
import requests

st.title("🚀 Painel de Controle de Integração")

# Botão para disparar o fluxo
if st.button("Disparar Fluxo de Integração"):
    with st.spinner("Chamando o Serviço A..."):
        try:
            # O frontend atua como um novo "cliente" que chama o seu Service A
            response = requests.get("http://localhost:8001/start")
            
            if response.status_code == 200:
                st.success("Fluxo concluído com sucesso!")
                st.json(response.json())
            else:
                st.error(f"Erro no fluxo: {response.status_code}")
        except Exception as e:
            st.error(f"Não foi possível conectar ao Serviço A: {e}")

# Exibir status do sistema
st.sidebar.header("Monitoramento")
if st.sidebar.button("Verificar Saúde dos Serviços"):
    col1, col2, col3 = st.columns(3)
    # Aqui você faria um GET em cada porta (8001, 8002, 8003) para checar o status
    col1.metric("Service A", "🟢 Online")
    col2.metric("Service B", "🟢 Online")
    col3.metric("Service C", "🟡 Instável")