import streamlit as st
from fpdf import FPDF
from datetime import date
import os # Biblioteca para verificar se o arquivo existe

# --- DADOS FIXOS DO DR. ELIÉSER ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- INTERFACE STREAMLIT ---
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

# --- LÓGICA DO PDF ---
if btn_gerar:
    pdf = FPDF()
    pdf.add_page()
    
    # --- CABEÇALHO COM LOGOTIPO ---
    y_inicial = pdf.get_y()
    
    # Inserir Logotipo (Lado Esquerdo)
    # Verifica se o arquivo logo.png existe no repositório antes de tentar inserir
    if os.path.exists("logo.png"):
        # pdf.image(nome_arquivo, x, y, largura, altura)
        # x=10 (margem esquerda), y=y_inicial, largura=25 (mm)
       # Procure esta linha e substitua por esta:
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, y_inicial - 5, w=25) # Adicionei o 'w=' para evitar conflitos de formato
    else:
        # Se não encontrar a imagem, avisa o usuário no Streamlit
        st.warning("⚠️ Arquivo 'logo.png' não encontrado no repositório. O PDF será gerado sem o logotipo.")

    # Informações do Veterinário (Lado Direito do Logotipo)
    # pdf.set_xy(x_inicial, y_inicial)
    pdf.set_xy(40, y_inicial) # Começa a escrever 40mm da margem esquerda
    pdf.set_font("Arial", 'B', 14)
    # pdf.cell(largura, altura, texto, ln, align)
    pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L') # Alinhado à esquerda do novo ponto X
    
    pdf.set_xy(40, pdf.get_y()) # Mantém o alinhamento X e vai para a próxima linha
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 6, txt=TITULO, ln=True, align='L')
    
    pdf.set_xy(40, pdf.get_y())
    pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
    
    pdf.set_xy(40, pdf.get_y())
    pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
    
    # Linha divisória abaixo de todo o cabeçalho
    pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5) 
    
    # --- DADOS DO ATENDIMENTO E PRESCRIÇÃO (Código anterior mantido) ---
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
    pdf.cell(0, 7, txt=f"Espécie: {especie}", ln=True)
    pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, txt=prescricao)
    
    # Assinatura do Veterinário (Código anterior mantido, mas reposicionado)
    pdf.ln(15)
    y_assinatura = pdf.get_y()
    pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
    pdf.set_font("Arial", '', 9)
    pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
    pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

    # --- RODAPÉ DIVIDIDO EM DUAS COLUNAS (Código anterior mantido) ---
    pdf.ln(15)
    y_inicial_rodape = pdf.get_y()
    
    # COLUNA ESQUERDA: Identificação do Comprador
    pdf.set_xy(10, y_inicial_rodape)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 6, txt="Identificação do Comprador", ln=False, align='C')
    
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(10, y_inicial_rodape + 6)
    pdf.cell(95, 5, txt="Nome: ________________________________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="Ident.: ______________ Org. Em: ________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="End: _________________________________", ln=True, align='C')
    pdf.set_x(10)
    pdf.cell(95, 5, txt="Cidade: ___________ UF: ___ Tel: ________", ln=True, align='C')
    
    # COLUNA DIREITA: Identificação do Fornecedor
    pdf.set_xy(105, y_inicial_rodape)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(95, 6, txt="Identificação do Fornecedor", ln=False, align='C')
    
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(105, y_inicial_rodape + 10) # Espaço para a linha de assinatura
    pdf.cell(95, 5, txt="________________________________", ln=True, align='C')
    pdf.set_x(105)
    pdf.cell(95, 5, txt="Assinatura do Farmacêutico", ln=True, align='C')
    pdf.set_x(105)
    pdf.cell(95, 5, txt="Data: ____ / ____ / ________", ln=True, align='C')

    # Saída do PDF
    # Tratamento de erro para encoding latin-1 (remove acentos se der erro, mas tenta manter)
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    st.download_button(label="📥 Baixar Receituário PDF", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
