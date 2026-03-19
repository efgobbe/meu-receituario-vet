import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import json

# Título da aba do navegador e nome do sistema atualizado
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Receituário Médico Veterinário")

# --- SISTEMA DE ARQUIVOS (FAVORITOS) ---
FAVORITOS_FILE = "favoritos.json"

def carregar_favoritos():
    if os.path.exists(FAVORITOS_FILE):
        try:
            with open(FAVORITOS_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def salvar_favorito(nome, dados):
    favs = carregar_favoritos()
    favs[nome] = dados
    with open(FAVORITOS_FILE, "w") as f:
        json.dump(favs, f)

def excluir_favorito(nome):
    favs = carregar_favoritos()
    if nome in favs:
        del favs[nome]
        with open(FAVORITOS_FILE, "w") as f:
            json.dump(favs, f)

if 'lista' not in st.session_state: 
    st.session_state.lista = []

# --- 1. BARRA LATERAL (GESTÃO DE FAVORITOS) ---
with st.sidebar:
    st.header("⭐ Modelos Salvos")
    favoritos = carregar_favoritos()
    if favoritos:
        selecionado = st.selectbox("Selecione um protocolo:", [""] + list(favoritos.keys()))
        if selecionado != "":
            if st.button("📥 Carregar"):
                st.session_state.lista = favoritos[selecionado]
                st.rerun()
            if st.button("🗑️ Excluir permanentemente"):
                excluir_favorito(selecionado)
                st.rerun()
    else:
        st.info("Nenhuma receita salva.")

# --- 2. IDENTIFICAÇÃO (LINHAS SEPARADAS) ---
paciente = st.text_input("Paciente:")
proprietario = st.text_input("Proprietário:")
especie_sel = st.selectbox("Espécie:", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])
data_hoje = date.today().strftime("%d/%m/%Y")

st.write("---")

# --- 3. PRESCRIÇÃO ---
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
            st.session_state.lista.append({"n": med_in, "q": q_in, "a": apres_in, "v": via_sel, "i": i_in})
            st.rerun()

# --- 4. LISTA ATUAL E SALVAR ---
if st.session_state.lista:
    st.subheader("Itens na Receita Atual:")
    for idx, it in enumerate(st.session_state.lista):
        st.write(f"**{idx+1}.** {it['n']} - {it['q']} {it['a']}")

    c1, c2 = st.columns([1, 2])
    if c1.button("🗑️ Limpar Lista Atual"):
        st.session_state.lista = []
        st.rerun()

    nome_fav = c2.text_input("Nome para salvar este modelo:", placeholder="Ex: Protocolo Giardíase")
    if c2.button("⭐ Salvar nos Favoritos"):
        if nome_fav:
            salvar_favorito(nome_fav, st.session_state.lista)
            st.success("Salvo!")
            st.rerun()

# --- 5. GERAÇÃO DO PDF ---
st.write("---")
if st.button("🚀 GERAR PDF (2 VIAS PAISAGEM)"):
    if not st.session_state.lista:
        st.error("Adicione itens à prescrição.")
    else:
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(False) 

        for ox in [0, 150]:
            if os.path.exists("logo.png"): pdf.image("logo.png", ox + 10, 10, w=20)
            pdf.set_font("Arial", 'B', 11); pdf.set_xy(ox + 35, 10)
            pdf.cell(100, 5, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'L')
            pdf.set_font("Arial", '', 8); pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Médico Veterinário - CRMV-SC 2754", 0, 1, 'L')
            pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Rua Isidoro Schilickmann, 93 - Braço do Norte - SC", 0, 1, 'L')
            
            pdf.ln(10); pdf.set_font("Arial", 'B', 10); pdf.set_x(ox + 10)
            pdf.cell(130, 5, f"Paciente: {paciente}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Espécie: {especie_sel}", 0, 1)
            
            pdf.ln(3); pdf.set_font("Arial", 'B', 10); pdf.set_x(ox + 10)
            pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            for it in st.session_state.lista:
                pdf.ln(1); pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} --- {it['q']} {it['a']} ({it['v']})", 0, 1)
                pdf.set_font("Arial", '', 9); pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"{it['i']}")
            
            pdf.set_y(148); pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_________________________________________", 0, 1, 'C')
            pdf.ln(2); pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8); pdf.set_
