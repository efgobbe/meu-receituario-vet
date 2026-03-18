import streamlit as st
from fpdf import FPDF
from datetime import date
import os

# --- DADOS DO VETERINÁRIO ---
NOME_VET = "Dr. Eliéser Ferreira Gobbe"
TITULO = "Médico Veterinário"
REGISTRO = "CRMV-SC 2754"
ENDERECO = "Rua Isidoro Schilickmann, 93-Santa Augusta"
CIDADE_ESTADO = "Braço do Norte - SC"
CPF_VET = "CPF: 272.814.978-06"

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário Profissional")

if 'lista_medicamentos' not in st.session_state:
    st.session_state.lista_medicamentos = []

# --- 1. PACIENTE ---
with st.expander("1. Identificação do Paciente", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("Nome do Animal")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
        peso = st.text_input("Peso (kg)", placeholder="Ex: 10.5")
    with c2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO ---
with st.expander("2. Adicionar Itens", expanded=True):
    col_v, col_m = st.columns([1, 2])
    with col_v:
        via = st.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    with col_m:
        medicamento = st.text_input("Medicamento")
    
    col_q, col_u, _ = st.columns([1, 1, 2])
    with col_q:
        qtd = st.selectbox("Qtd.", list(range(1, 11)))
    with col_u:
        un = st.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    
    instrucoes = st.text_area("Instruções")
    
    if st.button("➕ Adicionar Medicamento"):
        if medicamento and instrucoes:
            st.session_state.lista_medicamentos.append({
                "via": via, "nome": medicamento, "dose": instrucoes, "qtd": qtd, "un": un
            })
            st.success("Adicionado!")
        else:
            st.error("Preencha o nome e as instruções.")

if st.session_state.lista_medicamentos:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_medicamentos = []
        st.rerun()

# --- 3. PDF ---
if st.button("🚀 Gerar Receituário PDF"):
    if not st.session_state.lista_medicamentos:
        st.warning("Adicione itens à lista primeiro.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_at = pdf.get_y()
        
        # Logo
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y_at - 5, w=25)
            except: pass

        # Cabeçalho
        pdf.set_xy(40, y_at)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_font("Arial", '', 10)
        pdf.set_x(40)
        pdf.cell(0, 5, txt=TITULO, ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
        
        # Dados do Atendimento
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente} ({especie}) - Peso: {peso}kg", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Lista de Prescrição
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_medicamentos:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['nome']} --- {item['qtd']} {item['un']} ({item['via']})", ln=True)
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
        pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

        # Rodapé Técnico
        pdf.ln(10)
        yr = pdf.get_y()
        # Esquerda - Comprador
        pdf.set_xy(10, yr)
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(95, 5, txt="IDENTIFICAÇÃO DO COMPRADOR", ln=True, align='C')
        pdf.set_font("Arial", '', 7)
        pdf.set_x(10)
        pdf.cell(95, 4, txt="Nome: ____________________________________", ln=True, align='C')
        pdf.set_x(10)
        pdf.cell(95, 4, txt="End: _____________________________________", ln=True, align='C')
        # Direita - Fornecedor
        pdf.set_xy(105, yr)
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(95, 5, txt="IDENTIFICAÇÃO DO FORNECEDOR", ln=True, align='C')
        pdf.set_xy(105, yr + 8)
        pdf.cell(95, 4, txt="____________________________________", ln=True, align='C')
        pdf.set_x(105)
        pdf.cell(95, 4, txt="Assinatura do Farmacêutico", ln=True, align='C')

        # Saída do PDF
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 Baixar PDF Final", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
