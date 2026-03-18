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

# Inicializa a lista de medicamentos na memória
if 'lista_medicamentos' not in st.session_state:
    st.session_state.lista_medicamentos = []

# --- 1. IDENTIFICAÇÃO DO PACIENTE ---
with st.expander("1. Identificação do Paciente", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Ave", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. SEÇÃO DE PRESCRIÇÃO DETALHADA ---
with st.expander("2. Adicionar Itens à Prescrição", expanded=True):
    col_via, col_med = st.columns([1, 2])
    with col_via:
        via = st.selectbox("Via de Uso", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável", "Uso Retal", "Uso Inalatório"])
    
    with col_med:
        medicamento = st.text_input("Nome do Medicamento / Fármaco", placeholder="Ex: Simparic 20mg")
    
    # Campo separado para doses e instruções
    instrucoes = st.text_area("Dose e Instruções de Uso", placeholder="Ex: Administrar 1 comprimido, por via oral, a cada 30 dias.")
    
    if st.button("➕ Adicionar Medicamento"):
        if medicamento and instrucoes:
            # Organiza o texto que vai para a lista
            item_formatado = {
                "via": via,
                "nome": medicamento,
                "dose": instrucoes
            }
            st.session_state.lista_medicamentos.append(item_formatado)
            st.success(f"{medicamento} adicionado com sucesso!")
        else:
            st.error("Por favor, preencha o nome do medicamento e as instruções.")

# Exibição da Lista Atual
if st.session_state.lista_medicamentos:
    st.write("---")
    st.subheader("Itens Confirmados:")
    for i, item in enumerate(st.session_state.lista_medicamentos):
        st.markdown(f"**{i+1}. {item['nome']}** ({item['via']})")
        st.caption(f"Instruções: {item['dose']}")
    
    if st.button("🗑️ Limpar Toda a Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF ---
if st.button("🚀 Gerar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.warning("A lista de medicamentos está vazia.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_inicial = pdf.get_y()
        
        # Logotipo (se existir no GitHub)
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
        
        # Prescrições
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_medicamentos:
            # Nome do Medicamento em Negrito
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['nome']} ({item['via']})", ln=True)
            # Instruções em fonte normal
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['dose']}")
            pdf.ln(3)
        
        # Assinatura (Centralizada)
        pdf.ln(15)
        pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
        pdf.cell(0, 5,
