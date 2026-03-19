import streamlit as st
from fpdf import FPDF
from datetime import date
import os

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador de Receituário - 2 Vias")

if 'lista' not in st.session_state: st.session_state.lista = []

# --- 1. ENTRADA DE DADOS (INTERFACE) ---
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
    if st.form_submit_button("➕ Adicionar Medicamento"):
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

        for ox in [0, 150]: # Lado Esquerdo e Direito
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
            
            # CORPO DA RECEITA (Onde os dados aparecem preenchidos)
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {paciente} ({especie_sel})", 0, 1)
            pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            
            # Prescrição
            pdf.ln(3)
            pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.lista:
                pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} ({it['q']} un) - {it['v']}", 0, 1)
                pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"Inst: {it['i']}")
            
            # Assinatura Veterinário
            pdf.set_y(148)
            pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_" * 45, 0, 1
