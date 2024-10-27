import streamlit as st
from utils.auth import inicializar_admin
from components.login import exibir_login
from components.sidebar import menu_com_redirecionamento

def main():
    # Inicialização do estado da sessão
    if 'usuarios' not in st.session_state:
        st.session_state.usuarios = {}
        
    for key in ['autenticado', 'usuario', 'admin', 'pagina']:
        if key not in st.session_state:
            st.session_state[key] = False if key != 'pagina' else 'dashboard'

    st.set_page_config(
        page_title="Meu Aplicativo Streamlit",
        page_icon=":shark:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    inicializar_admin()

    if not st.session_state.autenticado:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
            </style>
            """, unsafe_allow_html=True)
        
        exibir_login()
    else:
        # Integrar o menu da sidebar
        menu_com_redirecionamento()

        # Botão de logout no canto superior direito
        col_logout = st.columns([6, 1])
        with col_logout[1]:
            if st.button("Sair"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        col1, col2, col3 = st.columns([1,2,1])
        
        with col2:
            st.title("👋 Bem-vindo ao Gerenciador de Tarefas!")
            
            st.write("Este é um aplicativo simples e eficiente para gerenciar suas tarefas diárias.")
            
            st.header("🌟 Principais funcionalidades:")
            
            st.markdown("""
            ✅ **Gerenciamento de Tarefas**: Crie, edite e exclua tarefas facilmente
            
            📅 **Organização por Data**: Visualize e filtre suas tarefas por data
            
            ⏰ **Controle de Horários**: Defina horários específicos para cada tarefa
            
            📊 **Estatísticas**: Acompanhe seu progresso com métricas de conclusão
            
            👥 **Multi-usuário**: Sistema seguro com login individual
            """)
        # Aqui você pode adicionar a lógica para exibir o conteúdo das páginas selecionadas no sidebar

if __name__ == "__main__":
    main()
