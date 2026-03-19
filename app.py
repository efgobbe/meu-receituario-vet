import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Receituário Profissional - 2 Vias")

if 'lista' not in st.session_state: st.session_state.lista = []

# --- ENTRADA DE DADOS ---
c1, c2 = st.columns(2)
pac = c1.text_input("Nome do Animal")
esp = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
prop = c2.text_input("Proprietário/Tutor")
data_h = date.today().strftime("%d/%m/%Y")

with st.form("f_med", clear_on_submit=True):
    col_a, col_b = st.columns([1, 2])
    via_sel = col_a.selectbox("Via de Administração", ["Uso Oral", "Uso Tópico", "Uso Injetável", "Uso Colírio"])
    med_in = col_b.text_input("Medicamento")
    q_in = st.number_input("Quantidade", min_value=1, value=1)
    i_in = st.text_area("Instruções de Uso")
    if st.form_submit_button("➕ Adicionar Medicamento"):
        if med_in and i_in:
            st.session_state.lista.append({"n": med_in, "q": q_in, "v": via_sel, "i": i_in})
            st.rerun()

if st.session_state.lista and st.button("🗑️ Limpar Lista"):
    st.session_state.lista = []
    st.rerun()

# --- FUNÇÃO DE GERAÇÃO DO PDF ---
if st.button("🚀 GERAR RECEITURÁRIO (2 VIAS PAISAGEM)"):
    if not st.session_state.lista:
        st.error("Adicione itens à prescrição.")
    else:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(False) # Garante folha única

        for ox in [0, 150]: # Lado Esquerdo (0) e Lado Direito (150)
            # 1. Logo e Cabeçalho
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
            
            # 2. Dados do Paciente e Espécie
            pdf.ln(8)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {pac} ({esp})", 0, 1) # Espécie incluída aqui
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Proprietário: {prop}", 0, 1)
            
            # 3. Prescrição
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.lista:
                pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} ({it['q']} un) - {it['v']}", 0, 1)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"Inst: {it['i']}")
            
            # 4. Campo de Assinatura do Veterinário (Fixado antes do rodapé)
            pdf.set_y(155)
            pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_" * 45, 0, 1, 'C')
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"Médico Veterinário - CRMV-SC 2754  |  Data: {data_h}", 0, 1, 'C')

            # 5. Rodapé (Comprador à Esquerda, Fornecedor à Direita)
            ry = 172
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 7)
            for L in ["Nome:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF:", "Tel:"]:
                pdf.set_x(ox + 10); pdf.cell(65, 3.5, L, 0, 1)
            
            pdf.set_xy(ox + 85, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 18)
            pdf.set_font("Arial", '', 7)
            pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85)
            pdf.cell(55, 4, f"Data: {data_h}", 0, 1, 'R')

        # Linha de corte central
        pdf.line(148.5, 5, 148.5, 205)
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITUÁRIO FINAL", pdf_out, "receita.pdf", "application/pdf")
