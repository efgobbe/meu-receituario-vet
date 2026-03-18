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

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="centered")
st.title("📋 Gerador de Receituário")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- INTERFACE DE PREENCHIMENTO ---
with st.form("form_dados"):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal", placeholder="Ex: elieser")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor", placeholder="Ex: lucifer")
        data_hoje = date.today().strftime("%d/%m/%Y")
    
    st.divider()
    st.subheader("Adicionar Medicamento")
    c_via, c_med = st.columns([1, 2])
    via_input = c_via.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
    med_input = c_med.text_input("Medicamento/Apresentação")
    
    c_qtd, c_un, _ = st.columns([1, 1, 2])
    qtd_input = c_qtd.selectbox("Qtd.", list(range(1, 11)))
    un_input = c_un.selectbox("Tipo", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
    
    inst_input = st.text_area("Instruções de Uso")
    
    add_item = st.form_submit_button("➕ Adicionar à Lista")
    if add_item:
        if med_input and inst_input:
            st.session_state.lista_meds.append({
                "via": via_input, "nome": med_input, "inst": inst_input, "qtd": qtd_input, "un": un_input
            })
            st.rerun()

# Exibição e Botão de Limpar
if st.session_state.lista_meds:
    st.write("---")
    for i, item in enumerate(st.session_state.lista_meds):
        st.text(f"{i+1}. {item['nome']} ({item['qtd']} {item['un']})")
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- GERAÇÃO DO PDF (FORMATO FIEL AO MODELO) ---
if st.button("🚀 Gerar e Baixar PDF"):
    if not st.session_state.lista_meds:
        st.error("Adicione ao menos um item.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_topo = pdf.get_y()
        
        # Logo (alinhada à esquerda)
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y_topo - 5, w=25)
            except: pass

        # Cabeçalho 
        pdf.set_xy(40, y_topo)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, txt=NOME_VET, ln=True, align='L')
        pdf.set_x(40)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, txt=TITULO, ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=f"{ENDERECO} - {CIDADE_ESTADO}", ln=True, align='L')
        pdf.set_x(40)
        pdf.cell(0, 5, txt=CPF_VET, ln=True, align='L')
        pdf.line(10, pdf.get_y() + 5, 200, pdf.get_y() + 5)
        
        # Dados do Paciente 
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, txt=f"Paciente: {paciente}", ln=True)
        pdf.cell(0, 7, txt=f"Espécie: {especie}", ln=True)
        pdf.cell(0, 7, txt=f"Proprietário: {proprietario}", ln=True)
        
        # Título Prescrição [cite: 7]
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="PRESCRIÇÃO:", ln=True)
        
        # Itens [cite: 8]
        for item in st.session_state.lista_meds:
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 7, txt=f"{item['nome']} --- {item['qtd']} {item['un']} ({item['via']})", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['inst']}")
            pdf.ln(3)
        
        # Bloco de Assinatura [cite: 17, 18]
        pdf.ln(15)
        pdf.cell(0, 0, txt="__________________________________________", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=NOME_VET, ln=True, align='C')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"{TITULO} - {REGISTRO}", ln=True, align='C')
        pdf.cell(0, 5, txt=f"Data: {data_hoje}", ln=True, align='C')

        # Rodapé Técnico (Comprador/Fornecedor) [cite: 9, 10, 13, 14, 19, 20]
        pdf.ln(10)
        y_rod = pdf.get_y()
        # Esquerda - Comprador [cite: 9]
        pdf.set_xy(10, y_rod)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(95, 6, txt="Identificação do Comprador", ln=True, align='C')
        pdf.set_font("Arial", '', 8)
        pdf.set_x(10); pdf.cell(95, 5, txt="Nome: ________________________________", ln=True, align='C')
        pdf.set_x(10); pdf.cell(95, 5, txt="Ident.: ______________ Org. Em: ________", ln=True, align='C')
        pdf.set_x(10); pdf.cell(95, 5, txt="End: _________________________________", ln=True, align='C')
        pdf.set_x(10); pdf.cell(95, 5, txt="Cidade: ___________ UF: ___ Tel: ________", ln=True, align='C')
        # Direita - Fornecedor [cite: 19]
        pdf.set_xy(105, y_rod)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(95, 6, txt="Identificação do Fornecedor", ln=True, align='C')
        pdf.set_xy(105, y_rod + 10)
        pdf.cell(95, 5, txt="________________________________", ln=True, align='C')
        pdf.set_x(105); pdf.cell(95, 5, txt="Assinatura do Farmacêutico", ln=True, align='C')
        pdf.set_x(105); pdf.cell(95, 5, txt="Data: ____ / ____ / ________", ln=True, align='C')

        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 Baixar PDF Final", data=pdf_bytes, file_name=f"receita_{paciente}.pdf", mime="application/pdf")
