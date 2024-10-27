import streamlit as st
import json
import os
import bcrypt
from utils.database import carregar_json, salvar_json
from components.sidebar import menu_com_redirecionamento

def carregar_usuarios():
    return carregar_json('usuarios.json')

def salvar_usuarios(usuarios):
    salvar_json('usuarios.json', usuarios)

def admin_panel():
    # Integra o menu da sidebar com verificação de autenticação e admin
    menu_com_redirecionamento()

    if not st.session_state.get('admin', False):
        st.error("Acesso negado. Você precisa ser um administrador para acessar esta página.")
        st.stop()



    st.title("Painel de Administração")

    usuarios = carregar_usuarios()

    st.subheader("Gerenciar Usuários")

    for usuario, dados in usuarios.items():
        with st.container():
            st.write(f"👤 {usuario}")
            st.write(f"Hash: {dados['senha'][:15]}...")
            st.write(f"Admin: {'Sim' if dados.get('admin', False) else 'Não'}")
            
            col1, col2, col3, col4 = st.columns([1,1,1,1])
            with col1:
                if st.button("✏️ Editar", key=f"edit_{usuario}", use_container_width=True):
                    st.session_state.usuario_editando = usuario
                    st.session_state.novo_nome = usuario
                    st.session_state.novo_admin = dados.get('admin', False)
            
            with col2:
                if usuario != "StrongerFX":
                    if st.button("🗑️ Excluir", key=f"del_{usuario}", use_container_width=True):
                        del usuarios[usuario]
                        salvar_usuarios(usuarios)
                        st.success(f"Usuário {usuario} excluído com sucesso!")
                        st.rerun()
            
            with col3:
                if st.button("🔑 Senha", key=f"pass_{usuario}", use_container_width=True):
                    st.session_state.alterando_senha = usuario

            with col4:
                if st.button("👤 Entrar", key=f"login_{usuario}", use_container_width=True):
                    st.session_state.autenticado = True
                    st.session_state.usuario = usuario
                    st.session_state.admin = dados.get('admin', False)
                    st.success(f"Você entrou na conta de {usuario}")
                    st.rerun()
            
            st.divider()

    if 'usuario_editando' in st.session_state:
        with st.form(key="editar_usuario_form"):
            st.subheader(f"Editando usuário: {st.session_state.usuario_editando}")
            novo_nome = st.text_input("Novo nome de usuário", value=st.session_state.novo_nome)
            novo_admin = st.checkbox("É administrador?", value=st.session_state.novo_admin)
            
            if st.form_submit_button("Salvar alterações", use_container_width=True):
                if st.session_state.usuario_editando != novo_nome:
                    usuarios[novo_nome] = usuarios.pop(st.session_state.usuario_editando)
                usuarios[novo_nome]['admin'] = novo_admin
                salvar_usuarios(usuarios)
                del st.session_state.usuario_editando
                st.success("Usuário atualizado com sucesso!")
                st.rerun()

    if 'alterando_senha' in st.session_state:
        with st.form(key="password_form"):
            st.subheader(f"Alterando senha: {st.session_state.alterando_senha}")
            nova_senha = st.text_input("Nova senha", type="password")
            confirmar_senha = st.text_input("Confirmar nova senha", type="password")
            
            if st.form_submit_button("Alterar senha", use_container_width=True):
                if nova_senha == confirmar_senha:
                    salt = bcrypt.gensalt()
                    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), salt)
                    usuarios[st.session_state.alterando_senha]['senha'] = senha_hash.decode('utf-8')
                    salvar_usuarios(usuarios)
                    del st.session_state.alterando_senha
                    st.success("Senha alterada com sucesso!")
                    st.rerun()
                else:
                    st.error("As senhas não coincidem!")

    st.divider()
    with st.expander("Adicionar Novo Usuário", expanded=False):
        with st.form(key="adicionar_usuario_form"):
            novo_usuario = st.text_input("Nome do usuário")
            nova_senha = st.text_input("Senha", type="password")
            confirmar_senha = st.text_input("Confirmar senha", type="password")
            is_admin = st.checkbox("É administrador?")
            
            if st.form_submit_button("Adicionar Usuário", use_container_width=True):
                if nova_senha != confirmar_senha:
                    st.error("As senhas não coincidem!")
                elif novo_usuario in usuarios:
                    st.error("Este usuário já existe!")
                else:
                    salt = bcrypt.gensalt()
                    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), salt)
                    usuarios[novo_usuario] = {'senha': senha_hash.decode('utf-8'), 'admin': is_admin}
                    salvar_usuarios(usuarios)
                    st.success(f"Usuário '{novo_usuario}' adicionado com sucesso!")
                    st.rerun()

if __name__ == "__main__":
    admin_panel()
