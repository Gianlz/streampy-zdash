import streamlit as st
from components.sidebar import menu_com_redirecionamento

def dashboard():
    # Integra o menu da sidebar
    menu_com_redirecionamento()


    st.title("Dashboard")
    st.write("Bem-vindo ao dashboard!")
    # Adicione mais elementos do Streamlit conforme necessário

    # Exemplo de estatísticas
    st.header("Estatísticas Gerais")
    # Aqui você pode adicionar gráficos, tabelas e outras visualizações

if __name__ == "__main__":
    dashboard()
