import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador de Receituário - 2 Vias")

if 'lista' not in st.session_state: 
    st.session_state.lista = []

# --- 1. IDENTIFICAÇÃO ---
paciente = st.text_input("Paciente:")
proprietario = st.text_input("Proprietário:")
especie_sel = st.selectbox("Espécie:", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])
data_hoje = date.today().strftime("%d/%m/%Y")

st.write("---")

# --- 2. PRESCRIÇÃO ---
with st.form("f_med", clear_on_submit=True):
    col_v, col_m = st.columns([1, 2])
    via_sel = col_v.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável", "Uso Otológico", "Uso Ocular"])
    med_in = col_m.text_input("Medicamento")
    
    col_q, col_a = st.columns(2)
    q_in = col_q.number_input("Quantidade", min_value=1, value=1)
    apres_in = col_a.selectbox("Apresentação", ["Cx", "Fr", "Cp", "Amp", "Bisn", "Env", "Tb", "Un", "Seringa", "Lata"])
    
    i_in = st.text_area("Instruções")
    
    if st.form_submit_button("➕ Adicionar Medicamento"):
        if med_in and i_in:
            st.session_state.lista.append({
                "n": med_in, "q": q_in, "a": apres_in, "v": via_sel, "i": i_in
            })
            st.rerun()

if st.session_state.lista:
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista = []
        st.rerun()

# --- 3. GERAÇÃO DO PDF ---
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
            
            # Dados Identificação
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Paciente: {paciente}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Espécie: {especie_sel}", 0, 1)
            
            # Prescrição
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10); pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            
            for it in st.session_state.lista:
                pdf.ln(1)
                pdf.set_font("Arial", 'B', 9)
                pdf.set_x(ox + 10)
                # Linha do Medicamento
                pdf.cell(130, 5, f"- {it['n']} --- {it['q']} {it['a']} ({it['v']})", 0, 1)
                
                # Instruções (SEM a palavra "Inst:")
                pdf.set_font("Arial", '', 9)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"{it['i']}") # Removido o prefixo aqui
            
            # Assinatura
            pdf.set_y(148)
            pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_________________________________________", 0, 1, 'C')
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_x(ox + 10); pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10); pdf.cell(130, 4, f"CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')

            # Rodapé
            ry = 162
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8); pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            for L in ["Nome:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF: SC", "Tel:"]:
                pdf.set_x(ox + 10); pdf.cell(65, 4, L, 0, 1)
            
            pdf.set_xy(ox + 85, ry)
            pdf.set_font("Arial", 'B', 8); pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22)
            pdf.set_font("Arial", '', 8); pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85); pdf.cell(55, 4, "Data: ____/____/____", 0, 1, 'R')

        pdf.line(148.5, 5, 148.5, 205)
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITUÁRIO", out, "receita.pdf", "application/pdf")
