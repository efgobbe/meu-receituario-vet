import streamlit as st
from fpdf import FPDF
from datetime import date
import os
import json

# Configuração da página
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")

# --- TÍTULO CENTRALIZADO ---
st.markdown("<h1 style='text-align: center;'>📋 Receituário Médico Veterinário</h1>", unsafe_allow_html=True)

# --- FUNÇÕES DE ARQUIVO ---
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
        json.dump(favs, f, indent=4)

def excluir_favorito(nome):
    favs = carregar_favoritos()
    if nome in favs:
        del favs[nome]
        with open(FAVORITOS_FILE, "w") as f:
            json.dump(favs, f, indent=4)

# --- INICIALIZAÇÃO DE ESTADOS ---
if 'lista' not in st.session_state: st.session_state.lista = []

# --- 1. BOTÃO NOVA RECEITA ---
if st.button("✨ NOVA RECEITA"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- 2. SEÇÃO FAVORITOS ---
favoritos = carregar_favoritos()
with st.expander("📂 MEUS MODELOS FAVORITOS", expanded=True):
    if favoritos:
        lista_nomes = [""] + list(favoritos.keys())
        selecionado = st.selectbox("Escolha um modelo para carregar:", lista_nomes)
        
        col1, col2 = st.columns(2)
        if selecionado:
            if col1.button("📥 CARREGAR ESTE MODELO"):
                dados = favoritos[selecionado]
                medicamentos = dados.get("medicamentos", [])
                st.session_state.lista = medicamentos
                
                if medicamentos:
                    pri = medicamentos[0]
                    st.session_state["med_val"] = pri.get("n", "")
                    st.session_state["via_val"] = pri.get("v", "Uso Oral")
                    st.session_state["qtd_val"] = pri.get("q", 1)
                    st.session_state["apres_val"] = pri.get("a", "Cx")
                    st.session_state["inst_val"] = pri.get("i", "")
                
                st.session_state["paciente_val"] = dados.get("paciente", "")
                st.session_state["prop_val"] = dados.get("proprietario", "")
                
                dados_c = dados.get("dados_comprador", {})
                st.session_state["c_nome_val"] = dados_c.get("nome", "")
                st.session_state["c_ident_val"] = dados_c.get("ident", "")
                st.session_state["c_end_val"] = dados_c.get("end", "")
                st.session_state["c_cid_val"] = dados_c.get("cid", "")
                st.session_state["c_uf_val"] = dados_c.get("uf", "")
                st.session_state["c_tel_val"] = dados_c.get("tel", "")
                
                st.success(f"✅ Modelo '{selecionado}' carregado!")
                st.rerun()
            
            if col2.button("🗑️ EXCLUIR ESTE MODELO"):
                excluir_favorito(selecionado)
                st.rerun()
    else:
        st.info("Nenhum modelo salvo.")

# --- 3. IDENTIFICAÇÃO ---
st.subheader("🐾 Identificação do Animal")
col_p1, col_p2 = st.columns(2)
paciente = col_p1.text_input("Paciente:", value=st.session_state.get("paciente_val", ""))
proprietario = col_p2.text_input("Proprietário:", value=st.session_state.get("prop_val", ""))
especie_sel = st.selectbox("Espécie:", ["Canina", "Felina", "Equina", "Bovina", "Ovina", "Caprina", "Suína", "Outra"])

with st.expander("👤 Dados do Comprador (Rodapé)", expanded=False):
    c_nome = st.text_input("Nome do Comprador:", value=st.session_state.get("c_nome_val", ""))
    c_ident = st.text_input("Identidade/CPF:", value=st.session_state.get("c_ident_val", ""))
    c_end = st.text_input("Endereço:", value=st.session_state.get("c_end_val", ""))
    col_c1, col_c2, col_c3 = st.columns([2, 1, 1])
    c_cid = col_c1.text_input("Cidade:", value=st.session_state.get("c_cid_val", ""))
    c_uf = col_c2.text_input("UF:", value=st.session_state.get("c_uf_val", ""), max_chars=2)
    c_tel = col_c3.text_input("Telefone:", value=st.session_state.get("c_tel_val", ""))

data_hoje = date.today().strftime("%d/%m/%Y")
st.write("---")

# --- 4. FORMULÁRIO DE MEDICAMENTOS ---
st.subheader("💊 Prescrição")
with st.form("f_med", clear_on_submit=True):
    col_v, col_m = st.columns([1, 2])
    vias = ["Uso Oral", "Uso Tópico", "Uso Injetável", "Uso Otológico", "Uso Ocular"]
    apres = ["Cx", "Fr", "Cp", "Amp", "Bisn", "Env", "Tb", "Un", "Seringa", "Lata"]
    
    v_idx = vias.index(st.session_state.get("via_val", "Uso Oral"))
    a_idx = apres.index(st.session_state.get("apres_val", "Cx"))
    
    via_sel = col_v.selectbox("Via", vias, index=v_idx)
    med_in = col_m.text_input("Medicamento", value=st.session_state.get("med_val", ""))
    
    col_q, col_a = st.columns(2)
    q_in = col_q.number_input("Quantidade", min_value=1, value=int(st.session_state.get("qtd_val", 1)))
    apres_in = col_a.selectbox("Apresentação", apres, index=a_idx)
    
    i_in = st.text_area("Instruções de Uso", value=st.session_state.get("inst_val", ""))
    
    if st.form_submit_button("➕ Adicionar à Lista"):
        if med_in and i_in:
            st.session_state.lista.append({"n": med_in, "q": q_in, "a": apres_in, "v": via_sel, "i": i_in})
            st.session_state["med_val"] = ""
            st.session_state["inst_val"] = ""
            st.rerun()

# --- 5. EXIBIÇÃO E SALVAMENTO ---
if st.session_state.lista:
    st.subheader("Itens na Receita Atual:")
    for idx, it in enumerate(st.session_state.lista):
        st.write(f"**{idx+1}.** {it['n']} - {it['q']} {it['a']}")
    
    if st.button("🗑️ Limpar Lista"):
        st.session_state.lista = []
        st.rerun()

    st.write("---")
    nome_fav = st.text_input("Nome do novo modelo favorito:")
    if st.button("⭐ SALVAR NOS FAVORITOS"):
        if nome_fav:
            salvar_favorito(nome_fav, {
                "paciente": paciente, "proprietario": proprietario,
                "medicamentos": st.session_state.lista,
                "dados_comprador": {"nome": c_nome, "ident": c_ident, "end": c_end, "cid": c_cid, "uf": c_uf, "tel": c_tel}
            })
            st.success("Modelo salvo!")
            st.rerun()

# --- 6. IMPRESSÃO ---
st.write("---")
if st.button("🖨️ IMPRIMIR RECEITA"):
    if not st.session_state.lista:
        st.error("Adicione medicamentos.")
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
            pdf.set_x(ox + 35); pdf.cell(100, 4, "Rua Isidoro Schilickmann, 93 - Braço do Norte - SC", 0, 1, 'L')
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
            pdf.set_font("Arial", '', 8); pdf.set_x(ox + 10)
            pdf.cell(130, 4, f"CRMV-SC 2754  |  Data: {data_hoje}", 0, 1, 'C')
            
            # --- RODAPÉ AJUSTADO ---
            ry = 162
            pdf.set_xy(ox + 10, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(65, 4, "Identificação do Comprador", 0, 1)
            pdf.set_font("Arial", '', 8)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Nome: {c_nome}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Ident./CPF: {c_ident}", 0, 1)
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"End: {c_end}", 0, 1)
            
            # Linha da Cidade e UF com espaço para caneta
            pdf.set_x(ox + 10)
            # Se a cidade estiver vazia, coloca pontilhado para caneta
            txt_cid = f"Cidade: {c_cid}" if c_cid else "Cidade: ......................................."
            pdf.cell(50, 4, txt_cid, 0, 0)
            
            pdf.set_x(ox + 65) 
            txt_uf = f"UF: {c_uf}" if c_uf else "UF: ......."
            pdf.cell(20, 4, txt_uf, 0, 1)
            
            pdf.set_x(ox + 10); pdf.cell(65, 4, f"Tel: {c_tel}", 0, 1)
            
            pdf.set_xy(ox + 85, ry); pdf.set_font("Arial", 'B', 8); pdf.cell(55, 4, "Identificação do Fornecedor", 0, 1, 'R')
            pdf.set_xy(ox + 85, ry + 22); pdf.set_font("Arial", '', 8); pdf.cell(55, 4, "Assinatura do Farmacêutico", 0, 1, 'R')
            pdf.set_x(ox + 85); pdf.cell(55, 4, "Data: ___/___/___", 0, 1, 'R')
            
        pdf.line(148.5, 5, 148.5, 205)
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 CLIQUE PARA ABRIR E IMPRIMIR", data=out, file_name=f"Receita_{paciente}.pdf", mime="application/pdf")
