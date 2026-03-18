import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS DO VETERINÁRIO ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 1. PACIENTE ---
with st.expander("1. Identificação", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with c2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Itens", expanded=True):
    v_col, m_col = st.columns([1, 2])
    with v_col:
        via = st.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    with m_col:
        med = st.text_input("Medicamento")
    
    q_col, u_col, _ = st.columns([1, 1, 2])
    with q_col:
        qtd = st.selectbox("Qtd.", list(range(1, 11)))
    with u_col:
        un = st.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    
    inst = st.text_area("Instruções")
    
    if st.button("➕ Adicionar"):
        if med and inst:
            st.session_state.lista_meds.append({"v": via, "n": med, "i": inst, "q": qtd, "u": un})
            st.success("Adicionado!")
        else:
            st.error("Preencha Medicamento e Instruções.")

if st.session_state.lista_meds:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- 3. PDF ---
if st.button("🚀 Gerar PDF"):
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
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
        
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente} ({especie})", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_meds:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['n']} --- {item['q']} {item['u']} ({item['v']})", ln=True)
            pdf.set_font("Arial", '', 1
