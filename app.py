import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import json
import urllib.parse

# 1. Configuração da página e PWA
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")

# Script para o PWA (manifesto e service worker)
st.markdown(
    """
    <link rel="manifest" href="manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js');
      }
    </script>
    """,
    unsafe_allow_html=True
)

# --- TÍTULO CENTRALIZADO ---
st.markdown("<h1 style='text-align: center;'>📋 Receituário Médico Veterinário</h1>", unsafe_allow_html=True)

# --- SISTEMA DE FAVORITOS ---
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

# --- BOTÃO NOVA RECEITA ---
if st.button("✨ NOVA RECEITA"):
    st.session_state.lista = []
    st.rerun()

# --- SEÇÃO FAVORITOS ---
favoritos = carregar_favoritos()
with st.expander("📂 FAVORITOS", expanded=False):
    if favoritos:
        selecionado = st.selectbox("Escolha um modelo:", [""] + list(favoritos.keys()), key="fav_top")
        col1, col2 = st.columns(2)
        if selecionado != "":
            if col1.button("📥 Carregar Modelo"):
                st.session_state.lista = favoritos[selecionado]
                st.success(f"✅ '{selecionado}' carregado!")
                st.rerun()
            if col2.button("🗑️ Excluir Modelo"):
                excluir_favorito(selecionado)
                st.rerun()
    else:
        st.info("Nenhum modelo salvo.")

# --- IDENTIFICAÇÃO ---
paciente = st.text_input("Paciente:")
proprietario = st.text_input("Proprietário:")
especie_sel = st.selectbox("Espécie:", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])
data_hoje = date.today().strftime("%d/%m/%Y")

st.write("---")

# --- PRESCRIÇÃO ---
with st.form("f_med", clear_on_submit=True):
    col_v, col_m = st.columns([1, 2])
    via_sel = col_v.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável", "Uso Otológico", "Uso Ocular"])
    med_in = col_m.text_input("Medicamento")
    
    col_q, col_a = st.columns(2)
    q_in = col_q.number_input("Quantidade", min_value=1, value=1)
    apres_in = col_a.selectbox("Apresentação", ["Cx", "Fr", "Cp", "Amp", "Bisn", "Env", "Tb", "Un", "Seringa", "Lata"])
    
    i_in = st.text_area("Instruções")
    
    if st.form_submit_button("➕ Adicionar à Lista"):
        if med_in and i_in:
            st.session_state.lista.append({"n": med_in, "q": q_in, "a": apres_in, "v": via_sel, "i": i_in})
            st.rerun()

# --- LISTA ATUAL E SALVAMENTO ---
if st.session_state.lista:
    st.subheader("Itens na Receita:")
    for idx, it in enumerate(st.session_state.lista):
        st.write(f"**{idx+1}.** {it['n']} - {it['q']} {it['a']}")

    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista = []
        st.rerun()

    nome_fav = st.text_input("Nomear modelo para salvar:")
    if st.button("⭐ SALVAR NOS FAVORITOS"):
        if nome_fav:
            salvar_favorito(nome_fav, st.session_state.lista)
            st.success(f"✅ Salvo!")

# --- BOTÕES DE SAÍDA (PDF E WHATSAPP) ---
st.write("---")
col_pdf, col_wa = st.columns(2)

with col_pdf:
    if st.button("🖨️ GERAR PDF"):
        if not st.session_state.lista:
            st.error("Lista vazia.")
        else:
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            for ox in [0, 150]:
                pdf.set_font("Arial", 'B', 11); pdf.set_xy(ox + 35, 10)
                pdf.cell(100, 5, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'L')
                pdf.set_font("Arial", '', 8); pdf.set_x(ox + 35)
                pdf.cell(100, 4, "CRMV-SC 2754", 0, 1, 'L')
                pdf.ln(10); pdf.set_font("Arial", 'B', 10); pdf.set_x(ox + 10)
                pdf.cell(130, 5, f"Paciente: {paciente} | Prop: {proprietario}", 0, 1)
                pdf.cell(130, 6, "PRESCRIÇÃO:", 0, 1)
                for it in st.session_state.lista:
                    pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
                    pdf.cell(130, 5, f"- {it['n']} ({it['v']})", 0, 1)
                    pdf.set_font("Arial", '', 9); pdf.set_x(ox + 15)
                    pdf.multi_cell(120, 4, f"{it['i']}")
            out = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("📥 BAIXAR/ABRIR PDF", out, f"Receita_{paciente}.pdf", "application/pdf")

with col_wa:
    if st.button("📱 ENVIAR VIA WHATSAPP"):
        if not st.session_state.lista:
            st.error("Lista vazia.")
        else:
            # Criando o texto para o WhatsApp
            texto = f"*RECEITUÁRIO MÉDICO VETERINÁRIO*\n"
            texto += f"*Dr. Eliéser Ferreira Gobbe - CRMV-SC 2754*\n\n"
            texto += f"*Paciente:* {paciente}\n"
            texto += f"*Proprietário:* {proprietario}\n"
            texto += f"----------------------------\n"
            for it in st.session_state.lista:
                texto += f"\n💊 *{it['n']}* ({it['v']})\n"
                texto += f"Qtd: {it['q']} {it['a']}\n"
                texto += f"Instruções: {it['i']}\n"
            
            # Codificando para URL
            texto_url = urllib.parse.quote(texto)
            link_wa = f"https://wa.me/?text={texto_url}"
            
            # Botão que abre o link
            st.markdown(f"""<a href="{link_wa}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #25D366; color: white; padding: 10px; text-align: center; border-radius: 5px;">
                                Abrir WhatsApp agora
                            </div></a>""", unsafe_allow_html=True)
