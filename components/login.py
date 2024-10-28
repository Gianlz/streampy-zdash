import streamlit as st
from utils.auth import verificar_credenciais, salvar_usuario

def exibir_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Login")
        
        tab_login, tab_cadastro = st.tabs(["Login", "Cadastro"])
        
        with tab_login:
            usuario_login = st.text_input("Usuário", key="login_user")
            senha = st.text_input("Senha", type="password")
            
            if st.button("Entrar"):
                autenticado, is_admin = verificar_credenciais(usuario_login, senha)
                if autenticado:
                    st.session_state.update({
                        'autenticado': True,
                        'usuario': usuario_login,
                        'admin': is_admin
                    })
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário não encontrado ou senha incorreta")
        
        with tab_cadastro:
            novo_usuario = st.text_input("Novo Usuário")
            nova_senha = st.text_input("Nova Senha", type="password")
            confirmar_senha = st.text_input("Confirmar Senha", type="password")
            
            if st.button("Cadastrar"):
                if not novo_usuario or not nova_senha:
                    st.error("Preencha todos os campos")
                elif nova_senha != confirmar_senha:
                    st.error("As senhas não coincidem")
                elif novo_usuario == "StrongerFX":
                    st.error("Este nome de usuário não está disponível")
                elif verificar_credenciais(novo_usuario, "")[0]:
                    st.error("Este usuário já existe!")
                else:
                    salvar_usuario(novo_usuario, nova_senha)
                    # Atualiza o estado da sessão após cadastro bem-sucedido
                    st.session_state.update({
                        'autenticado': True,
                        'usuario': novo_usuario,
                        'admin': False
                    })
                    st.success("Usuário cadastrado com sucesso!")
                    st.rerun()
