import streamlit as st
from fpdf import FPDF
from datetime import date

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Receituário 2 Vias - Paisagem")

if 'lista' not in st.session_state: st.session_state.lista = []

# --- ENTRADA DE DADOS ---
c1, c2 = st.columns(2)
pac = c1.text_input("Animal")
esp = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
prop = c2.text_input("Tutor")
data_h = date.today().strftime("%d/%m/%Y")

with st.form("f_med", clear_on_submit=True):
    col_a, col_b = st.columns([1, 2])
    v_in = col_a.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável"])
    m_in = col_b.text_input("Medicamento")
    q_in = st.number_input("Qtd", min_value=1, value=1)
    i_in = st.text_area("Instruções")
    if st.form_submit_button("➕ Adicionar"):
        if m_in and i_in:
            st.session_state.lista.append({"n": m_in, "q": q_in, "v": v_in, "i": i_in})
            st.rerun()

if st.session_state.lista and st.button("🗑️ Limpar"):
    st.session_state.lista = []
    st.rerun()

# --- GERAÇÃO DO PDF (2 VIAS LADO A LADO) ---
st.write("---")
if st.session_state.lista:
    if st.button("🚀 GERAR PDF PARA IMPRESSÃO"):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(False) # Impede quebra de página automática
        
        for ox in [0, 150]: # Offset 0 (esquerda) e 150 (direita)
            # Cabeçalho 
            pdf.set_font("Arial", 'B', 11)
            pdf.set_xy(ox + 10, 10)
            pdf.cell(130, 5, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Médico Veterinário - CRMV-SC 2754", 0, 1, 'C')
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Rua Isidoro Schilickmann, 93 - Braço do Norte - SC", 0, 1, 'C')
            
            # Paciente [cite: 1, 6]
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {pac} | Espécie: {esp}", 0, 1)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Proprietário: {prop} | Data: {data_h}", 0, 1)
            
            # Prescrição [cite: 7]
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.lista:
                pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} ({it['q']} un) - {it['v']}", 0, 1)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"Inst: {it['i']}")
            
            # Rodapé Comprador (Esquerda) [cite: 9, 10, 11, 12, 13, 14, 15, 16]
            ry = 160
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 7)
            for L in ["Nome:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF:", "Tel:"]:
                pdf.set_x(ox + 10); pdf.cell(65, 3.5, L, 0, 1)
            
            # Rodapé Fornecedor (Direita) [cite: 19, 20]
            pdf.set_xy(ox + 80, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(60, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 80, ry + 18)
            pdf.set_font("Arial", '', 7)
            pdf.cell(60, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 80)
            pdf.cell(60, 4, "Data: ____/____/____", 0, 1, 'R')

        # Linha de corte central
        pdf.line(148.5, 5, 148.5, 205)
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITA (2 VIAS)", pdf_out, "receita.pdf", "application/pdf")
