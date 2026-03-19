import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador de Receituário - 2 Vias")

if 'lista' not in st.session_state: st.session_state.lista = []

# --- 1. ENTRADA DE DADOS (DENTRO DO SITE) ---
c1, c2 = st.columns(2)
paciente = c1.text_input("Nome do Animal")
proprietario = c2.text_input("Proprietário/Tutor")
data_hoje = date.today().strftime("%d/%m/%Y")

with st.form("f_med", clear_on_submit=True):
    col_a, col_b = st.columns([1, 2])
    via_sel = col_a.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável"])
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

# --- 2. FUNÇÃO DE GERAÇÃO DO PDF ---
if st.button("🚀 GERAR PDF (2 VIAS PAISAGEM)"):
    if not st.session_state.lista:
        st.error("Adicione itens à prescrição.")
    else:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(False) 

        for ox in [0, 150]: # Lado Esquerdo (0) e Direito (150)
            # --- CABEÇALHO ---
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
            
            # --- CORPO DA RECEITA ---
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {paciente}", 0, 1)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            
            pdf.ln(3)
            pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.lista:
                pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} ({it['q']} un) - {it['v']}", 0, 1)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"Inst: {it['i']}")
            
            # --- ASSINATURA DO VETERINÁRIO (CENTRAL) ---
            pdf.set_y(148)
            pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_" * 45, 0, 1, 'C')
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"Médico Veterinário - CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')

            # --- RODAPÉ IDENTIFICAÇÃO (IGUAL AO ANEXO) ---
            ry = 162
            # Lado Esquerdo: Comprador
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            # A Espécie agora é um item da lista 
            labels = ["Nome:", "Espécie:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF:", "Tel:"]
            for L in labels:
                pdf.set_x(ox + 10); pdf.cell(65, 4, L, 0, 1)
            
            # Lado Direito: Fornecedor [cite: 19-20]
            pdf.set_xy(ox + 85, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22)
            pdf.set_font("Arial", '', 8)
            pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85)
            pdf.cell(55, 4, "Data: ____/____/____", 0, 1, 'R')

        # Linha de corte central
        pdf.line(148.5, 5, 148.5, 205)
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITUÁRIO FINAL", pdf_out, "receita.pdf", "application/pdf")
