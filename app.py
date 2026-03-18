import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS FIXOS DO PROFISSIONAL ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário Profissional")

# Inicializa a lista de medicamentos na memória do navegador
if 'lista_medicamentos' not in st.session_state:
    st.session_state.lista_medicamentos = []

# --- FORMULÁRIO DE IDENTIFICAÇÃO ---
with st.expander("1. Identificação do Paciente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- SEÇÃO DE PRESCRIÇÃO DINÂMICA ---
with st.expander("2. Adicionar Medicamentos", expanded=True):
    col_via, col_med = st.columns([1, 2])
    with col_via:
        via = st.selectbox("Via de Uso", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    with col_med:
        detalhes = st.text_area("Medicamento, Dose e Instruções", placeholder="Ex: Simparic 20mg - Dar 1 comprimido...")
    
    if st.button("➕ Adicionar à Receita"):
        if detalhes:
            item = f"({via}) \n{detalhes}"
            st.session_state.lista_medicamentos.append(item)
            st.success("Item adicionado!")
        else:
            st.warning("Preencha os detalhes do medicamento.")

# Exibe o que já foi adicionado
if st.session_state.lista_medicamentos:
    st.write("---")
    st.write("**Itens na Receita:**")
    for i, m in enumerate(st.session_state.lista_medicamentos):
        st.text(f"{i+1}. {m}")
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- GERAÇÃO DO PDF ---
if st.button("🚀 Gerar e Baixar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.error("Adicione pelo menos um medicamento antes de gerar.")
    else:
        pdf = FPDF()
        pdf.add_page()
        
        y_inicial = pdf.get_y()
        
        # Logotipo
        if os.path.exists("logo.png"):
            try:
                pdf.image("logo.png", 10, y_inicial - 5, w=25) 
            except:
                pass

        # Cabeçalho
        pdf.set_xy(40, y_inicial)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 6, txt=TITULO, ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5) 
        
        # Dados do Paciente
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente}   |   Especie: {especie}", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Prescrições acumuladas
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        pdf.set_font("Arial", '', 11)
        
        for item in st.session_state.lista_medicamentos:
            pdf.multi_cell(0, 7, txt=item)
            pdf.ln(3)
        
        # Assinatura
        pdf.ln(15)
        pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
        pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

        # Rodapé Técnico em Colunas
        pdf.ln(10)
        y_rodape = pdf.get_y()
        # Coluna Esquerda
        pdf.set_xy(10, y_rodape)
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(95, 5, txt="IDENTIFICAÇÃO DO COMPRADOR", ln=True, align='C')
        pdf.set_font("Arial", '', 7)
        pdf.set_x(10)
        pdf.cell(95, 4, txt="Nome: ____________________________________", ln=True, align='C')
        pdf.set_x(10)
        pdf.cell(95, 4, txt="Ident.: _______________ Org. Em: ___________", ln=True, align='C')
        pdf.set_x(10)
        pdf.cell(95, 4, txt="End: _____________________________________", ln=True, align='C')
        # Coluna Direita
        pdf.set_xy(105, y_rodape)
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(95, 5, txt="IDENTIFICAÇÃO DO FORNECEDOR", ln=True, align='C')
        pdf.set_xy(105, y_rodape + 8)
        pdf.cell(95, 4, txt="____________________________________", ln=True, align='C')
        pdf.set_x(105)
        pdf.cell(95, 4, txt="Assinatura do Farmacêutico", ln=True, align='C')

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 Baixar PDF Final", data=pdf_bytes, file_name=f"receita_{paciente}.pdf")
