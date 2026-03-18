import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS DO PROFISSIONAL ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário Profissional")

# Inicializa a lista de medicamentos na memória
if 'lista_medicamentos' not in st.session_state:
    st.session_state.lista_medicamentos = []

# --- 1. IDENTIFICAÇÃO DO PACIENTE ---
with st.expander("1. Identificação do Paciente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Ave", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. SEÇÃO DE PRESCRIÇÃO DETALHADA ---
with st.expander("2. Adicionar Itens à Prescrição", expanded=True):
    col_via, col_med = st.columns([1, 2])
    with col_via:
        via = st.selectbox("Via de Uso", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável", "Uso Retal", "Uso Inalatório"])
    
    with col_med:
        medicamento = st.text_input("Nome do Medicamento / Fármaco")
    
    instrucoes = st.text_area("Dose e Instruções de Uso")
    
    if st.button("➕ Adicionar Medicamento"):
        if medicamento and instrucoes:
            item_formatado = {"via": via, "nome": medicamento, "dose": instrucoes}
            st.session_state.lista_medicamentos.append(item_formatado)
            st.success(f"{medicamento} adicionado!")
        else:
            st.error("Preencha o nome e as instruções.")

# Exibição da Lista
if st.session_state.lista_medicamentos:
    st.write("---")
    for i, item in enumerate(st.session_state.lista_medicamentos):
        st.markdown(f"**{i+1}. {item['nome']}** ({item['via']})")
    
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF ---
if st.button("🚀 Gerar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.warning("Adicione itens à lista primeiro.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_inicial = pdf.get_y()
        
        # Logotipo
        if os.path.exists("logo.png"):
            try:
                pdf.image("logo.png", 10, y_inicial - 5, w=25) 
            except:
                pass

        # Cabeçalho
        pdf.set_xy(40, y_inicial)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
