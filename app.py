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

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador - 2 Vias Paisagem")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 1. PACIENTE ---
with st.expander("1. Identificação", expanded=True):
    c1, c2 = st.columns(2)
    paciente = c1.text_input("Animal")
    especie = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    proprietario = c2.text_input("Tutor")
    data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Medicamentos", expanded=True):
    with st.form("form_med", clear_on_submit=True):
        cv, cm = st.columns([1, 2])
        v_in = cv.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
        m_in = cm.text_input("Medicamento")
        cq, cu = st.columns(2)
        q_in = cq.number_input("Qtd", min_value=1, value=1)
        u_in = cu.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
        i_in = st.text_area("Instruções")
        if st.form_submit_button("➕ Adicionar"):
            if m_in and i_in:
                # Corrigido: Nomes das chaves batendo com a função de desenho
                st.session_state.lista_meds.append({
                    "n": m_in, "q": q_in, "u": u_in, "v": v_in, "i": i_in
                })
                st.rerun()

if st.session_state.lista_meds and st.button("🗑️ Limpar Lista"):
    st.session_state.lista_meds = []
    st.rerun()

def desenhar_via(pdf, ox, texto_via):
    # Cabeçalho Centralizado
    pdf.set_font("Arial", 'B', 11)
    pdf.set_xy(ox + 10, 10)
    pdf.cell(130, 6, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=TIT_VET, ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=END_VET + " - " + CID_VET, ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=CPF_VET, ln=True, align='C')
    
    # Identificação da Via
    pdf.ln(2)
    pdf.set_x(ox + 5)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(135, 5, txt=f"--- {texto_via} ---", ln=True, align='C')
    pdf.line(ox + 5, pdf.get_y(), ox + 140, pdf.get_y())

    # Dados do Paciente
    pdf.ln(4)
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
        # Lendo as chaves corretas: n, q, u, v, i
        linha = f"{it['n']} - {it['q']} {it['u']} ({it['v']})"
        pdf.cell(0, 5, txt=linha, ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.set_x(ox + 10)
        pdf.multi_cell(125, 4, txt=f"Instruções: {it['i']}")
        pdf.ln(1)
    
    # Assinatura Veterinário
    pdf.set_y(145)
    pdf.set_x(ox + 10)
    pdf.cell(130, 0, txt="_" * 45, ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.set_x(ox + 10)
    # Linha CRMV e Data juntas para poupar espaço
    pdf.cell(130, 4, txt=f"{TIT_VET} - {REG_VET} - Data: {data_hoje}", ln=True, align='C')

    # Rodapé Original
    ry = 165
    pdf.set_font("Arial", 'B', 8)
    pdf.set_xy(ox + 10, ry)
    pdf.cell(65, 4, txt="Identificação do Comprador", ln=True)
    pdf.set_font("Arial", '', 8)
    # Rótulos idênticos ao anexo
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="Nome:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="Org. Em:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="Ident.:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="End:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="Cidade:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="UF:", ln=True)
    pdf.set_x(ox+10); pdf.cell(65, 4, txt="Tel:", ln=True)
    
    # Fornecedor
