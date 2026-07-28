# frontend/app.py

import streamlit as st
import requests
from datetime import datetime

# 1. Configuração da Página e Estilização Customizada (Light Mode Moderno)
st.set_page_config(
    page_title="ControlTask - Gerenciador de Tarefas",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS para customizar as cores e suavizar o contraste visual
st.markdown("""
    <style>
    /* Estilização do fundo e fontes globais */
    .stApp {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #1E293B !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    p, label {
        color: #475569 !important;
    }
    /* Customização dos Cards de Métricas */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* Estilização de linhas de tarefas */
    .task-row {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #CBD5E1;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .priority-high { border-left-color: #FCA5A5; }
    .priority-medium { border-left-color: #FED7AA; }
    .priority-low { border-left-color: #BAE6FD; }
    </style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://127.0.0.1:8000"

# 2. Inicialização do Estado da Sessão (Session State)
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "screen" not in st.session_state:
    st.session_state.screen = "login"


# =========================================================================
# FUNÇÕES DE INTERAÇÃO COM A API (BACKEND)
# =========================================================================

def login_user(email, password):
    # No MVP atual, buscamos ou validamos via criação/simulação de fluxo
    # Como não criamos rota de login específica na Sprint 1, vamos emular o login
    # buscando a lista de usuários ou criando um fluxo de ID direto para fins de teste funcional
    try:
        # Criamos uma lógica amigável: se o usuário tentar logar, buscamos se ele existe na rota de usuários
        # Para simplificar a experiência de teste da Aula 2, se digitar dados válidos, damos acesso de teste.
        if email and password:
            st.session_state.user_id = 1  # Usuário padrão de teste do SQLite
            st.session_state.user_name = email.split("@")[0].capitalize()
            st.session_state.screen = "dashboard"
            st.rerun()
    except Exception:
        st.error("Erro ao conectar com o servidor.")

def register_user(name, email, password):
    try:
        response = requests.post(f"{API_BASE_URL}/users", json={
            "name": name,
            "email": email,
            "password": password
        })
        if response.status_code == 201:
            st.success("Conta criada com sucesso! Faça login para continuar.")
            return True
        else:
            st.error(response.json().get("detail", "Erro ao cadastrar."))
            return False
    except Exception:
        st.error("Não foi possível conectar ao Backend. Verifique se a API está rodando.")
        return False

def get_tasks():
    try:
        response = requests.get(f"{API_BASE_URL}/users/{st.session_state.user_id}/tasks")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def add_task(title, description, priority):
    try:
        response = requests.post(f"{API_BASE_URL}/users/{st.session_state.user_id}/tasks", json={
            "title": title,
            "description": description,
            "priority": priority
        })
        return response.status_code == 201
    except Exception:
        st.error("Erro ao salvar tarefa.")
        return False

def update_task_status(task_id, current_title, current_priority, new_status):
    try:
        requests.put(f"{API_BASE_URL}/tasks/{task_id}", json={
            "title": current_title,
            "priority": current_priority,
            "status": new_status
        })
        st.rerun()
    except Exception:
        st.error("Erro ao atualizar tarefa.")

def delete_task_action(task_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
        if response.status_code == 204:
            st.rerun()
    except Exception:
        st.error("Erro ao excluir tarefa.")


# =========================================================================
# TELAS / VIEWS
# =========================================================================

# --- TELA DE LOGIN / CADASTRO ---
if st.session_state.screen == "login":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>ControlTask</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Gerenciamento inteligente focado em produtividade leve</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["Acessar Conta", "Novo Cadastro"])
        
        with tab1:
            login_email = st.text_input("E-mail", key="login_email_input")
            login_pwd = st.text_input("Senha", type="password", key="login_pwd_input")
            if st.button("Entrar no Painel", type="primary", use_container_width=True):
                if login_email and login_pwd:
                    login_user(login_email, login_pwd)
                else:
                    st.warning("Preencha todos os campos.")
                    
        with tab2:
            reg_name = st.text_input("Nome Completo", key="reg_name")
            reg_email = st.text_input("E-mail", key="reg_email")
            reg_pwd = st.text_input("Senha Segura", type="password", key="reg_pwd")
            if st.button("Concluir Cadastro", use_container_width=True):
                if reg_name and reg_email and reg_pwd:
                    if register_user(reg_name, reg_email, reg_pwd):
                        st.balloons()
                else:
                    st.warning("Todos os campos são obrigatórios.")

# --- TELA DO DASHBOARD PRINCIPAL ---
elif st.session_state.screen == "dashboard":
    # Barra de Navegação Superior Leve
    nav_col1, nav_col2 = st.columns([4, 1])
    with nav_col1:
        st.markdown(f"## Olá, {st.session_state.user_name}! 👋")
        st.markdown("<p style='color: #64748B; margin-top:-15px;'>Aqui está o panorama da sua produtividade para hoje.</p>", unsafe_allow_html=True)
    with nav_col2:
        if st.button("Sair / Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.screen = "login"
            st.rerun()

    st.markdown("---")
    
    # Coleta de tarefas do banco de dados
    lista_tarefas = get_tasks()
    total_tasks = len(lista_tarefas)
    pendentes = len([t for t in lista_tarefas if t["status"] != "COMPLETED"])
    concluidas = total_tasks - pendentes

    # Linha 1: Cards Indicadores Visualmente Leves
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_tasks}</div><div class="metric-label">Total de Tarefas</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #EA580C;">{pendentes}</div><div class="metric-label">Em Aberto</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #16A34A;">{concluidas}</div><div class="metric-label">Concluídas</div></div>', unsafe_allow_html=True)

    # Linha 2: Área de Trabalho Dinâmica (Esquerda: Cadastro | Direita: Listagem)
    body_col1, body_col2 = st.columns([1.2, 2])
    
    with body_col1:
        st.markdown("### ➕ Nova Tarefa")
        with st.container(border=True):
            t_title = st.text_input("O que precisa ser feito?", placeholder="Ex: Estudar Engenharia de Software")
            t_desc = st.text_area("Notas / Subtarefas (Opcional)", placeholder="Detalhes da demanda...", height=80)
            t_prio = st.selectbox("Nível de Prioridade", ["LOW", "MEDIUM", "HIGH"])
            
            # Botão de IA posicionado sutilmente (simulação visual para a Aula 2)
            st.markdown("<p style='font-size:0.8rem; color:#A1A1AA; margin-bottom: 2px;'>Recursos inteligentes (Aula 3):</p>", unsafe_allow_html=True)
            ia_cols = st.columns(2)
            with ia_cols[0]:
                st.button("✨ Detalhar com IA", disabled=True, use_container_width=True)
            with ia_cols[1]:
                st.button("🤖 Priorizar com IA", disabled=True, use_container_width=True)
                
            st.write("")
            if st.button("Salvar Tarefa", type="primary", use_container_width=True):
                if t_title:
                    if add_task(t_title, t_desc, t_prio):
                        st.toast("Tarefa adicionada com sucesso!", icon="🎉")
                        st.rerun()
                else:
                    st.warning("O título da tarefa é obrigatório.")

    with body_col2:
        st.markdown("### 📋 Suas Demandas")
        
        if not lista_tarefas:
            st.info("Nenhuma tarefa cadastrada ainda. Use o formulário ao lado para começar!")
        else:
            for task in lista_tarefas:
                prio_class = f"priority-{task['priority'].lower()}"
                status_emoji = "⏳" if task["status"] == "PENDING" else "⚙️" if task["status"] == "IN_PROGRESS" else "✅"
                
                # Renderização customizada de cada linha de tarefa
                st.markdown(f"""
                    <div class="task-row {prio_class}">
                        <strong style='font-size: 1.1rem; color: #1E293B;'>{status_emoji} {task['title']}</strong><br>
                        <small style='color: #64748B;'>Prioridade: {task['priority']} | Status: {task['status']}</small><br>
                        <p style='margin-top: 5px; font-size: 0.95rem; color: #475569;'>{task['description'] if task['description'] else '<i>Sem descrição fornecida.</i>'}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botões de Ação para cada tarefa agrupados em colunas
                btn_cols = st.columns([1.5, 1.5, 1, 4])
                with btn_cols[0]:
                    if task["status"] != "COMPLETED" and st.button("Concluir", key=f"done_{task['id']}"):
                        update_task_status(task["id"], task["title"], task["priority"], "COMPLETED")
                with btn_cols[1]:
                    if task["status"] == "PENDING" and st.button("Iniciar", key=f"start_{task['id']}"):
                        update_task_status(task["id"], task["title"], task["priority"], "IN_PROGRESS")
                with btn_cols[2]:
                    if st.button("❌", key=f"del_{task['id']}", help="Excluir tarefa permanentemente"):
                        delete_task_action(task["id"])
                st.write("") # Espaçador visual entre blocos de tarefas

#venv\Scripts\activate

#streamlit run frontend/app.py

#API FastAPI	http://localhost:8000
#Swagger	http://localhost:8000/docs
#Frontend Streamlit	http://localhost:8501
