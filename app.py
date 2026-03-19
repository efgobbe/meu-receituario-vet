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

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador de Receituário - 2 Vias (Paisagem)")

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

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Medicamentos", expanded=True):
    with st.form("form_med", clear_on_submit=True):
        c_via, c_med = st.columns([1, 2])
        via_in = c_via.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
        med_in = c_med.text_input("Medicamento")
        c_qtd, c_un, _ = st.columns([1, 1, 2])
        qtd_in = c_qtd.selectbox("Qtd.", list(range(1, 11)))
        un_in = c_un.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
        inst_in = st.text_area("Instruções")
        
        if st.form_submit_button("➕ Adicionar à Lista"):
            if med_in and inst_in:
                st.session_state.lista_meds.append({
                    "nome": med_in, "qtd": qtd_in, "unidade": un_in, "via": via_in, "instrucoes": inst_in
                })
                st.rerun()

if st.session_state.lista_meds:
    if st.button("🗑️ Limpar Toda a Lista"):
        st.session_state.lista_meds = []
        st.rerun()

def gerar_conteudo_via(pdf, x_offset, titulo_via):
    """Função interna para desenhar cada via individualmente"""
    y_start = 10
    
    # Logo e Cabeçalho
    if os.path.exists("logo.png"):
        try: pdf.image("logo.png", x_offset + 5, y_start, w=20)
        except: pass

    pdf.set_xy(x_offset + 30, y_start)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 5, txt=NOME_VET, ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.set_x(x_offset + 30)
    pdf.cell(0, 4, txt=TITULO, ln=True)
    pdf.set_x(x_offset + 30)
    pdf.cell(0, 4, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True)
    pdf.set_x(x_offset + 30)
    pdf.cell(0, 4, txt=CPF_VET, ln=True)
    
    # Identificação da Via
    pdf.set_xy(x_offset + 5, y_start + 22)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(130, 5, txt=f"--- {titulo_via} ---", ln=True, align='C')
    pdf.line(x_offset + 5, pdf.get_y(), x_offset + 135, pdf.get_y())

    # Dados Paciente
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(x_offset + 5)
    pdf.cell(0, 5, txt=f"Paciente: {paciente}", ln=True)
    pdf.set_x(x_offset + 5)
    pdf.cell(0, 5, txt=f"Espécie: {especie}", ln=True)
    pdf.set_x(x_offset + 5)
    pdf.cell(0, 5, txt=f"Proprietário: {proprietario}", ln=True)
    
    # Prescrição
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_x(x_offset + 5)
    pdf.cell(0, 7, txt="PRESCRIÇÃO:", ln=True)
    for item in st.session_state.lista_meds:
        pdf.set_font("Arial", 'B', 9)
        pdf.set_x(x_offset + 5)
        pdf.cell(0, 5, txt=f"{item['nome']} - {item['qtd']} {item['unidade']} ({item['via']})", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.set_x(x_offset + 5)
        pdf.multi_cell(130, 4, txt=f"Instruções: {item['instrucoes']}")
        pdf.ln(1)
    
    # Assinatura Vet
    pdf.ln(5)
    curr_y = pdf.get_y()
    pdf.set_xy(x_offset + 5, curr_y)
    pdf.cell(130, 0, txt="_" * 40, ln=True, align='C')
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(x_offset + 130, 4, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.cell(x_offset + 130, 4, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
    pdf.cell(x_offset + 130, 4, txt=f"Data: {data_hoje}", ln=True, align='C')

    # Rodapé Técnico
    pdf.ln(5)
    ry = pdf.get_y()
    # Comprador
    pdf.set_xy(x_offset + 5, ry)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(70, 4, txt="Identificação do Comprador", ln=True)
    pdf.set_font("Arial", '', 7)
    for label in ["Nome:", "Ident.:", "Org. Em:", "End:", "Cidade:", "UF:", "Tel:"]:
        pdf.set_x(x_offset + 5)
        pdf.cell(70, 3.5, txt=label, ln=True)
    
    # Fornecedor
    pdf.set_xy(x_offset +
