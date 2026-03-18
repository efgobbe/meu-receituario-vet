import streamlit as st
from fpdf import FPDF
from datetime import date

# --- CONFIGURAÇÕES FIXAS (Extraídas do seu documento) ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe" [cite: 3, 11]
TITULO = "Médico Veterinário" [cite: 4, 12]
REGISTRO = "CRMV-SC 2754" [cite: 13, 14]
ENDERECO = "Rua Isidoro Schilickmann, 93 - Santa Augusta" [cite: 5]
CIDADE_ESTADO = "Braço do Norte - SC" [cite: 6]
CPF_VET = "CPF: 272.814.978-06" [cite: 7]

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Sistema de Receituário - Dr. Eliéser", layout="centered")

st.title("🐾 Gerador de Receituário")
st.info(f"Profissional: {NOME_VET} | {REGISTRO}") [cite: 3, 13]

with st.form("dados_receita"):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Paciente") [cite: 8]
        especie = st.text_input("Espécie") [cite: 9]
    with col2:
        proprietario = st.text_input("Proprietário/Tutor") [cite: 10]
        data_hoje = date.today().strftime("%d/%m/%Y")

    st.divider()
    
    # Campo de prescrição
    prescricao = st.text_area("Prescrição Técnica (Medicamento, Dose, Frequência)", height=200)
    
    # Botão de Gerar
    btn_gerar = st.form_submit_button("Gerar Receituário PDF")

# --- LÓGICA DO PDF ---
if btn_gerar:
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Fixo (Centralizado)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, txt=NOME_VET, ln=True, align='C') [cite: 3]
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 6, txt=TITULO, ln=True, align='C') [cite: 4]
    pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='C') [cite: 5, 6]
    pdf.cell(0, 5, txt=CPF_VET, ln=True, align='C') [cite: 7]
    pdf.line(10, 42, 200, 42) # Linha divisória
    
    pdf.ln(15)

    # Dados do Atendimento
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, txt=f"Paciente: {paciente}", ln=True) [cite: 8]
    pdf.cell(0, 8, txt=f"Espécie: {especie}", ln=True) [cite: 9]
    pdf.cell(0, 8, txt=f"Proprietário: {proprietario}", ln=True) [cite: 10]
    
    pdf.ln(10)
    
    # Conteúdo da Prescrição
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, txt=prescricao)
    
    # Rodapé de Assinatura (Igual ao documento)
    pdf.ln(40)
    pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, txt=NOME_VET, ln=True, align='C') [cite: 11]
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C') [cite: 12, 13]
    pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

    # Seção Técnica (Comprador/Fornecedor) - Opcional no PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(95, 5, txt="[ ] Identificação do Comprador", border=0) [cite: 15]
    pdf.cell(95, 5, txt="[ ] Identificação do Fornecedor", ln=True) [cite: 16]

    # Gerar arquivo para baixar
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(label="📥 Baixar Receituário PDF", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
