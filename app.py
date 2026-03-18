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
        medicamento = st.text_input("Nome do Medicamento / Fármaco")
    
    # NOVOS CAMPOS: Quantidade e Apresentação
    col_qtd, col_un, col_vazio = st.columns([1, 1, 2])
    with col_qtd:
        quantidade = st.selectbox("Qtd.", list(range(1, 11)))
    with col_un:
        unidade = st.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    
    instrucoes = st.text_area("Dose e Instruções de Uso")
    
    if st.button("➕ Adicionar Medicamento"):
        if medicamento and instrucoes:
            item_formatado = {
                "via": via, 
                "nome": medicamento, 
                "dose": instrucoes,
                "qtd": quantidade,
                "un": unidade
            }
            st.session_state.lista_medicamentos.append(item_formatado)
            st.success(f"{medicamento} adicionado!")
        else:
            st.error("Preencha o nome e as instruções.")

# Exibição da Lista
if st.session_state.lista_medicamentos:
    st.write("---")
    for i, item in enumerate(st.session_state.lista_medicamentos):
        st.markdown(f"**{i+1}. {item['nome']}** --- {item['qtd']} {item['un']} ({item['via']})")
    
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF ---
if st.button("🚀 Gerar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.warning("Adicione itens à lista primeiro.")
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
        
        # Prescrições
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_medicamentos:
            pdf.set_font("Arial", 'B', 11)
            # Exibe: Nome do Medicamento ........... 2 Cx (Uso Oral)
            texto_med = f"{item['nome']} {'.' * 10} {item['qtd']} {item['un']} ({item['via']})"
            pdf.cell(0, 7, txt=texto_med, ln=True)
            
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['dose']}")
            pdf.ln(3)
        
        # Assinatura
        pdf.ln(15)
        pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
        pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align
