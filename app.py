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

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 1. IDENTIFICAÇÃO DO PACIENTE ---
with st.expander("1. Identificação do Paciente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO (COM LIMPEZA AUTOMÁTICA) ---
with st.expander("2. Adicionar Medicamentos", expanded=True):
    with st.form("form_med", clear_on_submit=True):
        c_via, c_med = st.columns([1, 2])
        v_input = c_via.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
        m_input = c_med.text_input("Medicamento")
        
        c_qtd, c_un, _ = st.columns([1, 1, 2])
        q_input = c_qtd.selectbox("Qtd.", list(range(1, 11)))
        u_input = c_un.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
        
        i_input = st.text_area("Instruções")
        
        if st.form_submit_button("➕ Adicionar à Lista"):
            if m_input and i_input:
                st.session_state.lista_meds.append({
                    "v": v_input, "n": m_input, "i": i_input, "q": q_input, "u": u_input
                })
                st.success("Adicionado!")
            else:
                st.error("Preencha o medicamento e instruções.")

if st.session_state.lista_meds:
    if st.button("🗑️ Limpar Toda a Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- 3. PDF ---
if st.button("🚀 Gerar e Baixar PDF"):
    if not st.session_state.lista_meds:
        st.warning("Adicione itens primeiro.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y = pdf.get_y()
        
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y - 5, w=25)
            except: pass

        pdf.set_xy(40, y)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 6, txt=TITULO, ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='
