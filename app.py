import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS DO DR. ELIÉSER ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- INTERFACE ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

with st.form("form_receita"):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal")
        especie = st.text_input("Espécie")
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

    st.divider()
    prescricao = st.text_area("Prescrição Técnica", height=150)
    btn_gerar = st.form_submit_button("Gerar Receituário PDF")

# Lógica que roda quando o botão é clicado
if btn_gerar:
    pdf = FPDF()
    pdf.add_page()
    
    y_inicial = pdf.get_y()
    
    # Tratamento da Imagem
    if os.path.exists("logo.png"):
        try:
            pdf.image("logo.png", 10, y_inicial - 5, w=25) 
        except:
            st.error("Erro ao ler o arquivo 'logo.png'.")
    
    # Posicionamento do Cabeçalho
    pdf.set_xy(40, y_inicial)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
    
    pdf.set_xy(40, pdf.get_y())
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 6, txt=TITULO, ln=True, align='L')
    
    pdf.set_xy(40, pdf.get_y())
    pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
    
    pdf.set_xy(40, pdf.get_y())
    pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
    
    pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5) 
    
    # Dados do Paciente
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
    pdf.cell(0, 7, txt=f"Espécie: {especie}", ln=True)
    pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
    
    # Texto da Prescrição
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, txt=prescricao)
    
    # Assinatura Veterinário
    pdf.ln(15)
    pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
    pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

    # Rodapé Técnico em Colunas
    pdf.ln(15)
    y_rodape = pdf.get_y()
    
    # Coluna Comprador
    pdf.set_xy(10, y_rodape)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 6, txt="Identificação do Comprador", ln=False, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(10, y_rodape + 6)
    pdf.cell(95, 5, txt="Nome: ________________________________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="Ident.: ______________ Org. Em: ________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="End: _________________________________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="Cidade: ___________ UF: ___ Tel: ________", ln=True, align='C')
    
    # Coluna Fornecedor
    pdf.set_xy(105, y_rodape)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 6, txt="Identificação do Fornecedor", ln=False, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(105, y_rodape + 10)
    pdf.cell(95, 5, txt="________________________________", ln=True, align='C')
    pdf.set_x(105)
    pdf.cell(95, 5, txt="Assinatura do Farmacêutico", ln=True, align='C')
    pdf.set_x(105)
    pdf.cell(95, 5, txt="Data: ____ / ____ / ________", ln=True, align='C')

    # Download do arquivo
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(label="📥 Baixar Receituário", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
