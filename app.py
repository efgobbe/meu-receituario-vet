import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TIT_VET = "Médico Veterinário"
REG_VET = "CRMV-SC 2754"
END_VET = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CID_VET = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 1. IDENTIFICAÇÃO ---
with st.expander("1. Identificação do Paciente", expanded=True):
    c1, c2 = st.columns(2)
    paciente = c1.text_input("Nome do Animal")
    especie = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    proprietario = c2.text_input("Proprietário/Tutor")
    data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Medicamentos", expanded=True):
    with st.form("form_med", clear_on_submit=True):
        cv, cm = st.columns([1, 2])
        v_in = cv.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
        m_in = cm.text_input("Medicamento")
        cq, cu, _ = st.columns([1, 1, 2])
        q_in = cq.selectbox("Qtd.", list(range(1, 11)))
        u_in = cu.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
        i_in = st.text_area("Instruções")
        if st.form_submit_button("➕ Adicionar"):
            if m_in and i_in:
                st.session_state.lista_meds.append({
                    "n": m_in, "q": q_in, "u": u_in, "v": v_in, "i": i_in
                })
                st.rerun()

if st.session_state.lista_meds:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- 3. PDF ---
if st.session_state.lista_meds:
    pdf = FPDF()
    pdf.add_page()
    y = pdf.get_y()
    
    if os.path.exists("logo.png"):
        try: pdf.image("logo.png", 10, y - 5, w=25)
        except: pass

    pdf.set_xy(40, y)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, txt=NOME_VET, ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.set_x(40)
    pdf.cell(0, 6, txt=TIT_VET, ln=True)
    pdf.set_x(40)
    pdf.cell(0, 5, txt=f"{END_VET} - {CID_VET}", ln=True)
    pdf.set_x(40)
    pdf.cell(0, 5, txt=CPF_VET, ln=True)
    pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
    
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
    pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
    
    for item in st.session_state.lista_meds:
        pdf.set_font("Arial", 'B', 11)
        txt_m = f"{item.get('n')} - {item.get('q')} {item.get('u')}"
        pdf.cell(0, 7, txt=f"{txt_m} ({item.get('v')})", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 6, txt=f"Instruções: {item.get('i')}")
        pdf.ln(2)
    
    pdf.ln(10)
    pdf.cell(0, 0, txt="_" * 42, ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, txt=f"{TIT_VET} - {REG_VET}", ln=True, align='C')
    pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

    # RODAPÉ JUSTIFICADO (Linhas curtas para evitar erro)
    pdf.ln(10)
    yr = pdf.get_y()
    pdf.set_font("Arial", 'B', 9)
    pdf.set_xy(10, yr)
    pdf.cell(95, 6, txt="Identificação do Comprador", ln=True)
    pdf.set_font("Arial", '', 8)
    
    # Comprador
    pdf.set_x(10)
    pdf.cell(95, 5, txt="Nome: " + "_"*50, ln=True)
    pdf.set_x(10)
    pdf.cell(95, 5, txt="End: " + "_"*52, ln=True)
    pdf.set_x(10)
    l3 = "Cidade: " + "_"*20 + " UF: " + "_"*2 + " Tel: " + "_"*12
    pdf.cell(95, 5, txt=l3, ln=True)
    pdf.set_x(10)
    pdf.cell(95, 5, txt="CPF: " + "_"*52, ln=True)
    
    # Fornecedor
    pdf.set_xy(110, yr)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(90, 6, txt="Identificação do Fornecedor", ln=True, align='R')
    pdf.set_xy(110, yr + 12)
    pdf.cell(90, 5, txt="_"*35, ln=True, align='R')
    pdf.set_x(110)
    pdf.cell(90, 5, txt="Assinatura Farmacêutico", ln=True, align='R')

    pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(
        label="📥 Baixar PDF",
        data=pdf_out,
        file_name=f"receita_{paciente}.pdf",
        mime="application/pdf"
    )
