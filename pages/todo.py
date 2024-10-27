import streamlit as st
import datetime
import pandas as pd
import json
import os
from components.sidebar import menu_com_redirecionamento

def salvar_tarefas(tarefas, usuario):
    os.makedirs('tarefas', exist_ok=True)
    arquivo = f'tarefas/{usuario}.json'
    with open(arquivo, 'w') as f:
        json.dump(tarefas.to_dict('records'), f, default=str)

def carregar_tarefas(usuario):
    colunas = ['Data', 'Hora', 'Tarefa', 'Concluída', 'Usuario']
    df_vazio = pd.DataFrame(columns=colunas)
    
    arquivo = f'tarefas/{usuario}.json'
    if not os.path.exists(arquivo):
        return df_vazio
        
    try:
        with open(arquivo, 'r') as f:
            dados = json.load(f)
            if not dados:
                return df_vazio
            df = pd.DataFrame(dados)
            df['Data'] = pd.to_datetime(df['Data']).dt.date
            df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.time
            return df
    except (json.JSONDecodeError, KeyError):
        return df_vazio

def todo():
    # Integra o menu da sidebar
    menu_com_redirecionamento()

    st.Page(todo, title="Gerenciador de Tarefas", icon=":material/logout:")
    st.title("Gerenciador de Tarefas")

    usuario_atual = st.session_state.get('usuario', '')
    if not usuario_atual:
        st.error("Erro ao identificar o usuário. Por favor, faça login novamente.")
        return

    if 'tarefas' not in st.session_state:
        st.session_state.tarefas = carregar_tarefas(usuario_atual)

    with st.expander("Adicionar Nova Tarefa", expanded=False):
        nova_tarefa = st.text_input("Descrição da tarefa")
        col1, col2 = st.columns(2)
        with col1:
            data_tarefa = st.date_input("Data", min_value=datetime.date.today())
        with col2:
            hora_tarefa = st.time_input("Hora")
        
        if st.button("Adicionar", use_container_width=True) and nova_tarefa:
            nova_linha = pd.DataFrame({
                'Data': [data_tarefa], 
                'Hora': [hora_tarefa], 
                'Tarefa': [nova_tarefa], 
                'Concluída': [False],
                'Usuario': [usuario_atual]
            })
            st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_linha], ignore_index=True)
            salvar_tarefas(st.session_state.tarefas, usuario_atual)
            st.success("Tarefa adicionada com sucesso!")
            st.rerun()

    st.subheader("Suas Tarefas")
    data_filtro = st.date_input("Filtrar tarefas por data", value=datetime.date.today())
    
    tarefas_filtradas = st.session_state.tarefas[
        (st.session_state.tarefas['Data'] == data_filtro) & 
        (st.session_state.tarefas['Usuario'] == usuario_atual)
    ].sort_values('Hora')

    for idx, tarefa in tarefas_filtradas.iterrows():
        with st.container():
            st.write(f"🕒 {tarefa['Hora'].strftime('%H:%M')} - {tarefa['Tarefa']}")
            
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.checkbox(
                    "Concluída",
                    value=tarefa['Concluída'],
                    key=f"check_{idx}"
                ):
                    st.session_state.tarefas.loc[idx, 'Concluída'] = True
                    salvar_tarefas(st.session_state.tarefas, usuario_atual)
                else:
                    st.session_state.tarefas.loc[idx, 'Concluída'] = False
                    salvar_tarefas(st.session_state.tarefas, usuario_atual)
                    
            with col2:
                if st.button("✏️ Editar", key=f"edit_{idx}", use_container_width=True):
                    st.session_state[f"editing_{idx}"] = True
            with col3:
                if st.button("🗑️ Excluir", key=f"delete_{idx}", use_container_width=True):
                    st.session_state.tarefas = st.session_state.tarefas.drop(idx)
                    salvar_tarefas(st.session_state.tarefas, usuario_atual)
                    st.rerun()
        
        if st.session_state.get(f"editing_{idx}", False):
            nova_tarefa = st.text_input("Editar tarefa", value=tarefa['Tarefa'], key=f"edit_input_{idx}")
            nova_hora = st.time_input("Editar hora", value=tarefa['Hora'], key=f"edit_time_{idx}")
            if st.button("💾 Salvar", key=f"save_edit_{idx}", use_container_width=True):
                st.session_state.tarefas.at[idx, 'Tarefa'] = nova_tarefa
                st.session_state.tarefas.at[idx, 'Hora'] = nova_hora
                salvar_tarefas(st.session_state.tarefas, usuario_atual)
                st.session_state[f"editing_{idx}"] = False
                st.success("Tarefa atualizada com sucesso!")
                st.rerun()

    st.divider()
    st.subheader("Estatísticas")
    tarefas_usuario = st.session_state.tarefas[st.session_state.tarefas['Usuario'] == usuario_atual]
    total_tarefas = len(tarefas_usuario)
    tarefas_concluidas = len(tarefas_usuario[tarefas_usuario['Concluída']])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de tarefas", total_tarefas)
    with col2:
        st.metric("Tarefas concluídas", tarefas_concluidas)
    
    if total_tarefas > 0:
        st.progress(tarefas_concluidas / total_tarefas, text=f"{tarefas_concluidas}/{total_tarefas} concluídas")

if __name__ == "__main__":
    todo()
