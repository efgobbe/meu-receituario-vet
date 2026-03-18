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

# Inicializa a lista de medicamentos se não existir
if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 1. IDENTIFICAÇÃO (CAMPOS FIXOS NA TELA) ---
with st.expander("1. Identificação do Paciente e Tutor", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        paciente = st.text_input("Nome do Animal", key="pac_nome")
        especie = st.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
    with col2:
        proprietario = st.text_input("Proprietário/Tutor")
        data_hoje = date.today().strftime("%d/%m/%Y")

# --- 2. PRESCRIÇÃO (LIMPEZA AUTOMÁTICA) ---
with st.expander("2. Adicionar Medicamentos", expanded=True):
    # Usamos o st.form para agrupar e limpar ao enviar
    with st.form("form_medicamento", clear_on_submit=True):
        c_via, c_med = st.columns([1, 2])
        via_f = c_via.selectbox("Via de Uso", ["Uso Oral", "Uso Tópico", "Uso Ocular", "Uso Otológico", "Uso Injetável"])
        med_f = c_med.text_input("Nome do Medicamento / Apresentação")
        
        c_qtd, c_un, _ = st.columns([1, 1, 2])
        qtd_f = c_qtd.selectbox("Quantidade", list(range(1, 11)))
        un_f = c_un.selectbox("Unidade", ["Cx", "Fr", "Amp", "Bisn", "Env", "Un"])
        
        inst_f = st.text_area("Instruções de Uso")
        
        btn_add = st.form_submit_button("➕ Adicionar à Lista e Limpar Campos")
        
        if btn_add:
            if med_f and inst_f:
                st.session_state.lista_meds.append({
                    "via": via_f, "nome": med_f, "inst": inst_f, "qtd": qtd_f, "un": un_f
                })
                st.success(f"Item '{med_f}' adicionado!")
            else:
                st.error("Preencha o medicamento e as instruções.")

# Visualização da Lista Atual
if st.session_state.lista_meds:
    st.write("### Itens Confirmados:")
    for i, item in enumerate(st.session_state.lista_meds):
        st.markdown(f"**{i+1}. {item['nome']}** - {item['qtd']} {item['un']} ({item['via']})")
    
    if st.button("🗑️ Limpar Toda a Lista"):
        st.session_state.lista_meds = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF (FORMATO MODELO) ---
if st.button("🚀 Gerar e Baixar PDF Final"):
    if not st.session_state.lista_meds:
        st.warning("Adicione pelo menos um item à prescrição.")
    else:
        pdf = FPDF()
        pdf.add_page()
        y_ini = pdf.get_y()
        
        if os.path.exists("logo.png"):
            try: pdf.image("logo.png", 10, y_ini - 5, w=25)
            except: pass

        # Cabeçalho
        pdf.set_xy(40, y_ini)
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
        
        # Dados do Animal
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
            pdf.cell(0, 7, txt=f"{item['nome']} --- {item['qtd']} {item['un']} ({item['via']})", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, txt=f"Instruções: {item['inst']}")
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

        # Rodapé Comprador/Fornecedor
        pdf.ln(10)
        yr = pdf.get_y()
        pdf.set_xy(10, yr)
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(95, 6, txt="Identificação do Comprador", ln=True, align='C')
        pdf.set_font("Arial", '', 8)
        pdf.set_x(10); pdf.cell(95, 5, txt="Nome: ________________________________", ln=True, align='C')
        pdf.set_x(10); pdf.cell(95, 5, txt="Ident.: ______________ Org. Em: ________", ln=True, align='C')
        pdf.set_x(10); pdf.cell(
