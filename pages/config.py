import streamlit as st
from utils.database import salvar_json, carregar_json
import os
from components.sidebar import menu_com_redirecionamento

def Config():
    # Integra o menu da sidebar
    menu_com_redirecionamento()


    st.title("Configurações")
    
    # Carregar configurações existentes se houver
    config_path = 'config.json'
    if os.path.exists(config_path):
        config = carregar_json(config_path)
    else:
        config = {"tema": "Claro", "notificacoes": False}
    
    # Adicionar aqui as opções de configuração que você deseja
    st.write("Aqui você pode adicionar as opções de configuração do seu aplicativo.")
    
    # Exemplo de algumas configurações
    tema = st.selectbox("Selecione o tema", ["Claro", "Escuro"], index=["Claro", "Escuro"].index(config.get("tema", "Claro")))
    notificacoes = st.checkbox("Ativar notificações", value=config.get("notificacoes", False))
    
    if st.button("Salvar configurações"):
        config['tema'] = tema
        config['notificacoes'] = notificacoes
        salvar_json(config_path, config)
        st.success("Configurações salvas com sucesso!")

if __name__ == "__main__":
    Config()
