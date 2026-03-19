import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import json

st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Receituário Profissional com Favoritos")

# --- ARQUIVO DE BANCO DE DADOS ---
FAVORITOS_FILE = "favoritos.json"

def carregar_favoritos():
    if os.path.exists(FAVORITOS_FILE):
        with open(FAVORITOS_FILE, "r") as f:
            return json.load(f)
    return {}

def salvar_favorito(nome, dados):
    favs = carregar_favoritos()
    favs[nome] = dados
    with open(FAVORITOS_FILE, "w") as f:
        json.dump(favs, f)

# Inicialização da lista na sessão
if 'lista' not in st.session_state: st.session_state.lista = []

# --- 1. SEÇÃO DE FAVORITOS (CARREGAR) ---
with st.sidebar:
    st.header("⭐ Receitas Favoritas")
    favoritos = carregar_favoritos()
    if favoritos:
        receita_selecionada = st.selectbox("Escolha uma receita salva:", [""] + list(favoritos.keys()))
        if st.button("📥 Carregar Receita") and receita_selecionada != "":
            st.session_state.lista = favoritos[receita_selecionada]
            st.success(f"Receita '{receita_selecionada}' carregada!")
            st.rerun()
    else:
        st.info("Nenhuma receita salva ainda.")

# --- 2. IDENTIFICAÇÃO ---
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
    apres_in = col_a.selectbox("Apresentação", ["Cx", "Fr", "Cp", "Amp", "Bisn", "Env", "Tb", "Un", "Seringa"])
    
    i_in = st.text_area("Instruções")
    
    if st.form_submit_button("➕ Adicionar Medicamento"):
        if med_in and i_in:
            st.session_state.lista.append({"n": med_in, "q": q_in, "a": apres_in, "v": via_sel, "i": i_in})
            st.rerun()

# --- 4. GESTÃO DA LISTA ATUAL E SALVAR FAVORITO ---
if st.session_state.lista:
    st.subheader("Itens da Receita Atual:")
    for idx, it in enumerate(st.session_state.lista):
        st.write(f"**{idx+1}.** {it['n']} - {it['q']} {it['a']} ({it['v']})")

    c_limpar, c_fav = st.columns([1, 2])
    if c_limpar.button("🗑️ Limpar Lista"):
        st.session_state.lista = []
        st.rerun()

    # Campo para nomear e favoritar
    nome_fav = c_fav.text_input("Nome para salvar este protocolo:", placeholder="Ex: Otite Grave Canina")
    if c_fav.button("⭐ Salvar nos Favoritos"):
        if nome_fav:
            salvar_favorito(nome_fav, st.session_state.lista)
            st.success(f"Protocolo '{nome_fav}' salvo com sucesso!")
            st.rerun()
        else:
            st.warning("Dê um nome antes de favoritar.")

# --- 5. GERAÇÃO DO PDF (Código idêntico ao anterior) ---
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
            pdf.set_font("Arial", 'B', 11)
            pdf.set_xy(ox + 35, 10)
            pdf.cell(100, 5, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'L')
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Médico Veterinário - CRMV-SC 2754", 0, 1, 'L')
            pdf.set_x(ox + 35)
            pdf.cell(100, 4, "Rua Isidoro Schilickmann, 93 - Braço do Norte - SC", 0, 1, 'L')
            
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Paciente: {paciente}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Proprietário: {proprietario}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(130, 5, f"Espécie: {especie_sel}", 0, 1)
            
            pdf.ln(3)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10); pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
            for it in st.session_state.lista:
                pdf.ln(1); pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"- {it['n']} --- {it['q']} {it['a']} ({it['v']})", 0, 1)
                pdf.set_font("Arial", '', 9); pdf.set_x(ox + 15)
                pdf.multi_cell(120, 4, f"{it['i']}")
            
            pdf.set_y(148); pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_________________________________________", 0, 1, 'C')
            pdf.ln(2); pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8); pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')

            ry = 162
            pdf.set_xy(ox + 10, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            for L in ["Nome:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF: SC", "Tel:"]:
                pdf.set_x(ox + 10); pdf.cell(65, 4, L, 0, 1)
            
            pdf.set_xy(ox + 85, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22); pdf.set_font("Arial", '', 8); pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85); pdf.cell(55, 4, "Data: ____/____/____", 0, 1, 'R')

        pdf.line(148.5, 5, 148.5, 205)
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 BAIXAR RECEITUÁRIO", out, "receita.pdf", "application/pdf")
