import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador de Receituário - 2 Vias")

if 'lista' not in st.session_state: 
    st.session_state.lista = []

# --- 1. ENTRADA DE DADOS ---
# Organizado em 3 campos conforme solicitado
c1, c2 = st.columns(2)
paciente = c1.text_input("Nome do Animal")
proprietario = c2.text_input("Proprietário/Tutor")
# Espécie como terceiro campo, abaixo de Proprietário
especie_sel = c2.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])
data_hoje = date.today().strftime("%d/%m/%Y")

with st.form("f_med", clear_on_submit=True):
    col_a, col_b = st.columns([1, 2])
    via_sel = col_a.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável", "Uso Otológico", "Uso Ocular"])
    med_in = col_b.text_input("Medicamento")
    q_in = st.number_input("Quantidade", min_value=1, value=1)
    i_in = st.text_area("Instruções")
    if st.form_submit_button("➕ Adicionar"):
        if med_in and i_in:
            st.session_state.lista.append({"n": med_in, "q": q_in, "v": via_sel, "i": i_in})
            st.rerun()

if st.session_state.lista and st.button("🗑️ Limpar Lista"):
    st.session_state.lista = []
    st.rerun()

# --- 2. GERAÇÃO DO PDF ---
if st.button("🚀 GERAR PDF (2 VIAS PAISAGEM)"):
    if not st.session_state.lista:
        st.error("Adicione itens à prescrição.")
    else:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(False) 

        for ox in [0, 150]:
            # Cabeçalho
            if os.path.exists("logo.png"):
                pdf.image("logo.png", ox + 10, 10, w=20)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.set_xy(ox + 35, 10)
            pdf.cell(100, 5, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'L')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Médico Veterinário - CRMV-SC 2754", 0, 1, 'L')
            pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Rua Isidoro Schilickmann, 93 - Braço do Norte - SC", 0, 1, 'L')
            
            # Corpo (Dados preenchidos) [cite: 1-2, 6, 22-23]
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {paciente} ({especie_sel})", 0, 1)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            
            # Prescrição [cite: 7, 24-30]
            pdf.ln(3)
            pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.lista:
                pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} ({it['q']} un) - {it['v']}", 0, 1)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"Inst: {it['i']}")
            
            # Assinatura (Linha curta para evitar erro de sintaxe) [cite: 17-18, 39]
            pdf.set_y(148)
            pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_________________________________________", 0, 1, 'C')
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')

            # Rodapé (Apenas rótulos em branco) [cite: 9-16, 31-38, 51-53]
            ry = 162
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox+10); pdf.cell(65, 4, "Nome:", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "Org. Em:", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "Ident.:", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "End:", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "Cidade:", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "UF: SC", 0, 1)
            pdf.set_x(ox+10); pdf.cell(65, 4, "Tel:", 0, 1)
            
            # Fornecedor [cite: 19-20, 49-50, 54-55]
            pdf.set_xy(ox + 85, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22)
            pdf.set_font("Arial", '', 8)
            pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85)
            pdf.cell(55, 4, "Data: ____/____/____", 0, 1, 'R')

        pdf.line(148.5, 5, 148.5, 205)
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITUÁRIO", out, "receita.pdf", "application/pdf")
