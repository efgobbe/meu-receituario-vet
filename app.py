import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS ---
VET = "Dr. Eliéser Ferreira Gobbe"
CRMV = "CRMV-SC 2754"
INFO = "Rua Isidoro Schilickmann, 93-Santa Augusta\nBraço do Norte - SC | CPF: 272.814.978-06"

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

if 'meds' not in st.session_state:
    st.session_state.meds = []

# --- 1. PACIENTE ---
with st.expander("1. Identificação", expanded=True):
    c1, c2 = st.columns(2)
    paciente = c1.text_input("Nome do Animal")
    especie = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    tutor = c2.text_input("Proprietário")
    data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Itens", expanded=True):
    v_col, m_col = st.columns([1, 2])
    via = v_col.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    med = m_col.text_input("Medicamento")
    q_col, u_col, _ = st.columns([1, 1, 2])
    qtd = q_col.selectbox("Qtd.", list(range(1, 11)))
    un = u_col.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    inst = st.text_area("Instruções")
    
    if st.button("➕ Adicionar"):
        if med and inst:
            st.session_state.meds.append({"v": via, "n": med, "i": inst, "q": qtd, "u": un})
            st.rerun()

if st.session_state.meds:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.meds = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF ---
if st.button("🚀 Gerar PDF"):
    if not st.session_state.meds:
        st.warning("Adicione itens.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y = pdf.get_y()
        
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y-5, w=25)
            except: pass

        pdf.set_xy(40, y)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=VET, ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"Médico Veterinário - {CRMV}", ln=True)
        pdf.set_x(40)
        pdf.multi_cell(0, 5, txt=INFO)
        pdf.line(10, pdf.get_y()+2, 200, pdf.get_y()+2)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente} ({especie})", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {tutor}", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.meds:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['n']} - {item['q']} {item['u']} ({item['v']})", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['i']}")
            pdf.ln(2)
        
        pdf.ln(15)
        pdf.cell(0, 0, txt="_" * 40, ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, txt=VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{CRMV} | Data: {data_hoje}", ln=True, align='C')

        # Rodapé Simples
        pdf.ln(10)
        yr = pdf.get_y()
        pdf.set_font("Arial", 'B', 8)
        pdf.set_xy(10, yr); pdf.cell(95, 5, "COMPRADOR", 0, 0, 'C')
        pdf.set_xy(105, yr); pdf.cell(95, 5, "FORNECEDOR", 0, 0, 'C')
        pdf.set_xy(10, yr+10)
        pdf.cell(95, 5, "_" * 30, 0, 0, 'C')
        pdf.set_xy(105, yr+10)
        pdf.cell(95, 5, "_" * 30, 0, 0, 'C')

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 Baixar Receita", pdf_bytes, f"receita_{paciente}.pdf", "application/pdf")
