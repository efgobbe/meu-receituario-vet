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

# --- 2. PRESCRIÇÃO (LIMPEZA AUTOMÁTICA) ---
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
                    "nome": med_in,
                    "qtd": qtd_in,
                    "unidade": un_in,
                    "via": via_in,
                    "instrucoes": inst_in
                })
                st.success("Adicionado!")
            else:
                st.error("Preencha o medicamento e instruções.")

if st.session_state.lista_meds:
    st.write("---")
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
            try:
                pdf.image("logo.png", 10, y_topo - 5, w=25)
            except:
                pass

        # Cabeçalho
        pdf.set_xy(40, y_topo)
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
        
        # Dados Paciente
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
        pdf.cell(0, 7, txt=f"Espécie: {especie}", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Prescrição
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        for item in st.session_state.lista_meds:
            pdf.set_font("Arial", 'B', 11)
            n = item.get('nome', '')
            q = item.get('qtd', '')
            u = item.get('unidade', '')
            v = item.get('via', '')
            ins = item.get('instrucoes', '')
            
            linha = f"{n} --- {q} {u} ({v})"
            pdf.cell(0, 7, txt=linha, ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {ins}")
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

        # Rodapé Técnico Justificado
        pdf.ln(10)
        yr = pdf.get_y()
        
        # Lado Esquerdo - Comprador
        pdf.set_xy(10, yr)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(95, 6, txt="Identificação do Comprador", ln=True, align='L')
        pdf.set_font("Arial", '', 8)
        pdf.set_x(10)
        pdf.cell(95, 5, txt="Nome: " + "_" * 78, ln=True, align='L')
        pdf.set_x(10)
        pdf.cell(95, 5, txt="Ident.: " + "_" * 35 + " Org. Em: " + "_" * 25, ln=True, align='L')
        pdf.set_x(10)
        pdf.cell(95, 5, txt="End: " + "_" * 81, ln=True, align='L')
        pdf.set_x(10)
        pdf.cell(95, 5, txt="Cidade: " + "_" * 35 + " UF: " + "_" * 4 + " Tel: " + "_" * 19, ln=True, align='L')
        pdf.set_x(10)
        pdf.cell(95, 5, txt="CPF: " + "_" * 81, ln=True, align='L')
        
        # Lado Direito - Fornecedor
        pdf.set_xy(105, yr)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(95, 6, txt="Identificação do Fornecedor", ln=True, align='R')
        pdf.set_xy(105, yr + 15)
        pdf.cell(95, 5, txt="________________________________", ln=True, align='R')
        pdf.set_x(105)
        pdf.cell(95, 5, txt="Assinatura do Farmacêutico", ln=True, align='R')
        pdf.set_x(105)
        pdf.cell(95, 5, txt="Data: ____/____/________", ln=True, align='R')

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 Baixar PDF Final", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
