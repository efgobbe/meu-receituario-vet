import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import json

# Configuração da página
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")

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

def salvar_favorito(nome, dados_completos):
    favs = carregar_favoritos()
    favs[nome] = dados_completos
    with open(FAVORITOS_FILE, "w") as f:
        json.dump(favs, f)

def excluir_favorito(nome):
    favs = carregar_favoritos()
    if nome in favs:
        del favs[nome]
        with open(FAVORITOS_FILE, "w") as f:
            json.dump(favs, f)

# Inicialização de estados
if 'lista' not in st.session_state: st.session_state.lista = []
if 'comprador' not in st.session_state: st.session_state.comprador = {}

# --- 1. BOTÃO NOVA RECEITA ---
if st.button("✨ NOVA RECEITA"):
    st.session_state.lista = []
    st.session_state.comprador = {}
    st.rerun()

# --- 2. SEÇÃO FAVORITOS ---
favoritos = carregar_favoritos()
with st.expander("📂 FAVORITOS (Modelos Salvos)", expanded=False):
    if favoritos:
        selecionado = st.selectbox("Escolha um modelo:", [""] + list(favoritos.keys()), key="fav_top")
        col1, col2 = st.columns(2)
        if selecionado != "":
            if col1.button("📥 Carregar Modelo"):
                dados = favoritos[selecionado]
                st.session_state.lista = dados.get("medicamentos", [])
                st.session_state.comprador = dados.get("dados_comprador", {})
                st.success(f"✅ '{selecionado}' carregado!")
                st.rerun()
            if col2.button("🗑️ Excluir Modelo"):
                excluir_favorito(selecionado)
                st.rerun()
    else:
        st.info("Nenhum modelo salvo.")

# --- 3. IDENTIFICAÇÃO DO PACIENTE ---
st.subheader("🐾 Identificação do Animal")
col_p1, col_p2 = st.columns(2)
paciente = col_p1.text_input("Paciente:", value=st.session_state.get('paciente_val', ""))
proprietario = col_p2.text_input("Proprietário:")
especie_sel = st.selectbox("Espécie:", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])

# --- 4. IDENTIFICAÇÃO DO COMPRADOR (NOVIDADE) ---
with st.expander("👤 Dados do Comprador (Rodapé do PDF)", expanded=False):
    c_nome = st.text_input("Nome do Comprador:", value=st.session_state.comprador.get("nome", ""))
    c_ident = st.text_input("Identidade/CPF:", value=st.session_state.comprador.get("ident", ""))
    c_end = st.text_input("Endereço:", value=st.session_state.comprador.get("end", ""))
    col_c1, col_c2 = st.columns(2)
    c_cid = col_c1.text_input("Cidade:", value=st.session_state.comprador.get("cid", ""))
    c_tel = col_c2.text_input("Telefone:", value=st.session_state.comprador.get("tel", ""))
    
    # Atualiza o estado para salvar em favoritos
    st.session_state.comprador = {"nome": c_nome, "ident": c_ident, "end": c_end, "cid": c_cid, "tel": c_tel}

data_hoje = date.today().strftime("%d/%m/%Y")
st.write("---")

# --- 5. PRESCRIÇÃO ---
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

# --- 6. LISTA ATUAL E SALVAMENTO ---
if st.session_state.lista:
    st.subheader("Itens na Receita:")
    for idx, it in enumerate(st.session_state.lista):
        st.write(f"**{idx+1}.** {it['n']} - {it['q']} {it['a']}")

    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista = []
        st.rerun()

    nome_fav = st.text_input("Nomear modelo para salvar (Salva medicamentos + Comprador):")
    if st.button("⭐ SALVAR NOS FAVORITOS"):
        if nome_fav:
            dados_para_salvar = {
                "medicamentos": st.session_state.lista,
                "dados_comprador": st.session_state.comprador
            }
            salvar_favorito(nome_fav, dados_para_salvar)
            st.success(f"✅ Modelo '{nome_fav}' salvo com sucesso!")

# --- 7. GERAÇÃO DO PDF ---
st.write("---")
if st.button("🖨️ IMPRIMIR RECEITA"):
    if not st.session_state.lista:
        st.error("Adicione medicamentos primeiro.")
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
            
            # Rodapé e Assinatura
            pdf.set_y(148); pdf.set_x(ox + 10)
            pdf.cell(130, 0, "_________________________________________", 0, 1, 'C')
            pdf.ln(2); pdf.set_font("Arial", 'B', 9); pdf.set_x(ox + 10)
            pdf.cell(130, 4, "Dr. Eliéser Ferreira Gobbe", 0, 1, 'C')
            pdf.set_font("Arial", '', 8); pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')

            # IDENTIFICAÇÃO DO COMPRADOR PREENCHIDA NO PDF
            ry = 162
            pdf.set_xy(ox + 10, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Nome: {c_nome}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Ident./CPF: {c_ident}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"End: {c_end}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Cidade: {c_cid}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"UF: SC  Tel: {c_tel}", 0, 1)
            
            pdf.set_xy(ox + 85, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22); pdf.set_font("Arial", '', 8); pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85); pdf.cell(55, 4, f"Data: ___/___/___", 0, 1, 'R')

        pdf.line(148.5, 5, 148.5, 205)
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        st.download_button(label="📥 CLIQUE PARA ABRIR E IMPRIMIR", data=out, file_name=f"Receita_{paciente}.pdf", mime="application/pdf")
