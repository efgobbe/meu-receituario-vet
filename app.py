import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- CONFIGURAÇÃO E DADOS ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")

NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TIT_VET = "Médico Veterinário"
REG_VET = "CRMV-SC 2754"
END_VET = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CID_VET = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

st.title("📋 Gerador de Receituário - 2 Vias")

# --- FORMULÁRIO ---
with st.expander("1. Dados do Paciente", expanded=True):
    c1, c2 = st.columns(2)
    paciente = c1.text_input("Nome do Animal")
    especie = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    proprietario = c2.text_input("Proprietário")
    data_hoje = date.today().strftime("%d/%m/%Y")

with st.expander("2. Adicionar Medicamentos", expanded=True):
    with st.form("form_med", clear_on_submit=True):
        f1, f2 = st.columns([1, 2])
        via = f1.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável"])
        med = f2.text_input("Medicamento")
        f3, f4 = st.columns(2)
        qtd = f3.number_input("Qtd", min_value=1, value=1)
        un = f4.selectbox("Tipo", ["Cx", "Fr", "Un"])
        inst = st.text_area("Instruções")
        if st.form_submit_button("➕ Adicionar"):
            if med and inst:
                st.session_state.lista_meds.append({"n": med, "q": qtd, "u": un, "v": via, "i": inst})
                st.rerun()

if st.session_state.lista_meds:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- FUNÇÃO DO PDF ---
def desenhar_via(pdf, ox, titulo_via):
    # Cabeçalho
    pdf.set_font("Arial", 'B', 11)
    pdf.set_xy(ox + 10, 10)
    pdf.cell(130, 6, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=TIT_VET, ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=f"{END_VET} - {CID_VET}", ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=CPF_VET, ln=True, align='C')
    
    # Via
    pdf.ln(2)
    pdf.set_x(ox + 5)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(135, 5, txt=f"--- {titulo_via} ---", ln=True, align='C')
    pdf.line(ox + 5, pdf.get_y(), ox + 140, pdf.get_y())

    # Paciente
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(ox + 10)
    pdf.cell(0, 5, txt=f"Paciente: {paciente}", ln=True)
    pdf.set_x(ox + 10)
    pdf.cell(0, 5, txt=f"Proprietário: {proprietario}", ln=True)
    
    # Prescrição
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(ox + 10)
    pdf.cell(0, 6, txt="PRESCRIÇÃO:", ln=True)
    for it in st.session_state.lista_meds:
        pdf.set_font("Arial", 'B', 9)
        pdf.set_x(ox + 10)
        pdf.cell(0, 5, txt=f"{it['n']} - {it['q']} {it['u']} ({it['v']})", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.set_x(ox + 10)
        pdf.multi_cell(125, 4, txt=f"Instruções: {it['i']}")
        pdf.ln(1)
    
    # Assinatura centralizada
    pdf.set_y(150)
    pdf.set_x(ox + 10)
    pdf.cell(130, 0, txt="_" * 45, ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=f"{TIT_VET} - {REG_VET} - Data: {data_hoje}", ln=True, align='C')

    # Rodapé idêntico ao anexo
    ry = 170
    pdf.set_font("Arial", 'B', 8)
