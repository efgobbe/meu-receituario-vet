import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário Profissional")

if 'lista_medicamentos' not in st.session_state:
    st.session_state.lista_medicamentos = []

# --- 1. PACIENTE ---
with st.expander("1. Identificação do Paciente", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with c2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Itens", expanded=True):
    col_v, col_m = st.columns([1, 2])
    with col_v:
        via = st.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    with col_m:
        medicamento = st.text_input("Medicamento")
    
    col_q, col_u, _ = st.columns([1, 1, 2])
    with col_q:
        qtd = st.selectbox("Qtd.", list(range(1, 11)))
    with col_u:
        un = st.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    
    instrucoes = st.text_area("Instruções")
    
    if st.button("➕ Adicionar"):
        if medicamento and instrucoes:
            st.session_state.lista_medicamentos.append({
                "via": via, "nome": medicamento, "dose": instrucoes, "qtd": qtd, "un": un
            })
            st.success("Adicionado!")
        else:
            st.error("Preencha todos os campos.")

if st.session_state.lista_medicamentos:
    st.write("---")
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- 3. PDF ---
if st.button("🚀 Gerar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.warning("Lista vazia.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_pos = pdf.get_y()
        
        # Logo
        if os.path.exists("logo.png"):
            try:
                pdf.image("logo.png", 10, y_pos - 5, w=25)
            except:
                pass

        # Cabeçalho
        pdf.set_xy(40, y_pos)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 5, txt=TITULO, ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
        
        # Linha Divisória (Corrigida)
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
        
        # Dados do Paciente
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente}   |   Especie: {especie}", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Prescrição
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_medicamentos:
            pdf.set_font("Arial", 'B', 1
