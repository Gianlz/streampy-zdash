import streamlit as st

def menu_autenticado():
    # Menu para usuários autenticados
    st.sidebar.page_link("main.py", label="Página Inicial")
    st.sidebar.page_link("pages/todo.py", label="Lista de Tarefas")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
    st.sidebar.page_link("pages/config.py", label="Configurações")
    
    if st.session_state.get('admin', False):
        st.sidebar.page_link("pages/admin_panel.py", label="Painel de Administração")

def menu_nao_autenticado():
    # Menu para usuários não autenticados
    st.sidebar.page_link("main.py", label="Entrar")

def menu():
    # Determina se o usuário está logado e mostra o menu apropriado
    if not st.session_state.get('autenticado', False):
        menu_nao_autenticado()
        return
    menu_autenticado()

def menu_com_redirecionamento():
    # Redireciona usuários não logados para página principal
    if not st.session_state.get('autenticado', False):
        st.switch_page("main.py")
    menu()
