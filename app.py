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

# --- 3. GERAÇÃO DO PDF ---
if st.button("🚀 Gerar e Baixar PDF"):
    if not st.session_state.lista_meds:
        st.warning("Adicione medicamentos primeiro.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_topo = pdf.get_y()
        
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y_topo - 5, w=25)
            except: pass

        # Cabeçalho [cite: 3, 4, 5]
        pdf.set_xy(40, y_topo)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 6, txt=TITULO, ln=True)
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True)
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True)
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
        
        # Dados Paciente [cite: 1, 2, 6]
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
        pdf.cell(0, 7, txt=f"Espécie: {especie}", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Prescrição [cite: 7, 8]
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        for item in st.session_state.lista_meds:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['nome']} --- {item['qtd']} {item['unidade']} ({item['via']})", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['instrucoes']}")
            pdf.ln(2)
        
        # Assinatura Veterinário [cite: 17, 18]
        pdf.ln(10)
        pdf.cell(0, 0, txt="_" * 45, ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, txt=NOME_VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
        pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

        # RODAPÉ - CÓPIA FIEL DOS ANEXOS [cite: 9-16, 19-20, 29-36, 39-40]
        pdf.ln(10)
        y_final = pdf.get_y()
        
        # --- Lado Esquerdo: Identificação do Comprador ---
        pdf.set_xy(10, y_final)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(95, 7, txt="Identificação do Comprador", ln=True) # [cite: 9, 29]
        pdf.set_font("Arial", '', 10)
        pdf.cell(95, 6, txt="Nome:", ln=True) # [cite: 10, 30]
        pdf.cell(95, 6, txt="Ident.:", ln=True) # [cite: 11, 32]
        pdf.cell(95, 6, txt="Org. Em:", ln=True) # [cite: 12, 31]
        pdf.cell(95, 6, txt="End:", ln=True) # [cite: 13, 33]
        pdf.cell(95, 6, txt="Cidade:", ln=True) # [cite: 14, 34]
        pdf.cell(95, 6, txt="UF:", ln=True) # [cite: 15, 35]
        pdf.cell(95, 6, txt="Tel:", ln=True) # [cite: 16, 36]
        
        # --- Lado Direito: Identificação do Fornecedor ---
        # Posicionado exatamente na mesma altura do título do comprador
        pdf.set_xy(120, y_final)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(80, 7, txt="Identificação do Fornecedor", ln=True) # [cite: 19, 39]
        
        # Espaço para assinatura e campos finais à direita
        pdf.set_xy(120, y_final + 25) 
        pdf.set_font("Arial", '', 10)
        pdf.cell(80, 6, txt="Assinatura do Farmacêutico", ln=True) # 
        pdf.set_x(120)
        pdf.cell(80, 6, txt="Data:", ln=True) # 

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 Baixar PDF Final", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
