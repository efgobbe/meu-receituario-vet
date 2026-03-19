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
                st.session_state.lista_meds.append({"n": m_in, "q": q_in, "u": u_in, "v": v_in, "i": i_in})
                st.rerun()

if st.session_state.lista_meds and st.button("🗑️ Limpar Lista"):
    st.session_state.lista_meds = []
    st.rerun()

def desenhar_via(pdf, ox, texto_via):
    # ox é o offset X (0 para esquerda, 148.5 para direita)
    pdf.set_font("Arial", 'B', 11)
    # Cabeçalho simplificado para evitar cortes
    pdf.set_xy(ox + 10, 10)
    pdf.cell(130, 6, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=TIT_VET, ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=END_VET, ln=True, align='C')
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=CPF_VET, ln=True, align='C')
    
    # Linha e Tipo de Via
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
    pdf.set_x(ox + 10)
    pdf.cell(0, 6, txt="PRESCRIÇÃO:", ln=True)
    for it in st.session_state.lista_meds:
        pdf.set_font("Arial", 'B', 9)
        pdf.set_x(ox + 10)
        txt_m = f"{it['n']} - {it['q']} {it['u']} ({it['v']})"
        pdf.cell(0, 5, txt=txt_m, ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.set_x(ox + 10)
        pdf.multi_cell(125, 4, txt=f"Inst: {it['i']}")
        pdf.ln(1)
    
    # Assinatura Veterinário
    pdf.set_y(150)
    pdf.set_x(ox + 10)
    pdf.cell(130, 0, txt="_" * 40, ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 9)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.set_x(ox + 10)
    pdf.cell(130, 4, txt=f"{TIT_VET} - {REG_VET} - Data: {data_hoje}", ln=True, align='C')

    # Rodapé Comprador/Fornecedor [cite: 9-16, 19-20]
    ry = 170
    pdf.set_font("Arial", 'B', 8)
    pdf.set_xy(ox + 10, ry)
    pdf.cell(65, 4, txt="Identificação do Comprador", ln=True)
    pdf.set_font("Arial", '', 7)
    labels = ["Nome:", "Ident:", "Org. Em:", "End:", "Cidade:", "UF:", "Tel:"]
    for lab in labels:
        pdf.set_x(ox + 10)
        pdf.cell(65, 3.5, txt=lab, ln=True)
    
    # Fornecedor
    pdf.set_xy(ox + 80, ry)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(60, 4, txt="Identificação do Fornecedor", ln=True, align='R')
    pdf.set_xy(ox + 80, ry + 15)
    pdf.set_font("Arial", '', 7)
    pdf.cell(60, 4, txt="Assinatura Farmacêutico", ln=True, align='R')
    pdf.set_x(ox + 80)
    pdf.cell(60, 4, txt="Data: ____/____/____", ln=True, align='R')

# --- GERAR PDF ---
if st.button("🖨️ Gerar 2 Vias Paisagem"):
    if not st.session_state.lista_meds:
        st.warning("Adicione itens.")
    else:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        desenhar_via(pdf, 0, "1ª VIA: PACIENTE") # Esquerda
        pdf.line(148.5, 5, 148.5, 205) # Divisória
        desenhar_via(pdf, 148.5, "2ª VIA: FARMÁCIA") # Direita
        
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="💾 Baixar PDF", data=out, file_name="receita.pdf", mime="application/pdf")
