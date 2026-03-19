import streamlit as st
from fpdf import FPDF
from datetime import date

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Sistema Dr. Eliéser", layout="wide")
st.title("📋 Gerador - 2 Vias Paisagem")

if 'lista_meds' not in st.session_state:
    st.session_state.lista_meds = []

# --- 2. ENTRADA DE DADOS ---
c1, c2 = st.columns(2)
paciente = c1.text_input("Animal")
especie = c1.selectbox("Espécie", ["Canina", "Felina", "Equina", "Bovina", "Outra"])
proprietario = c2.text_input("Tutor")
data_hoje = date.today().strftime("%d/%m/%Y")

with st.form("form_med", clear_on_submit=True):
    f1, f2 = st.columns([1, 2])
    via = f1.selectbox("Via", ["Uso Oral", "Uso Tópico", "Uso Injetável"])
    med = f2.text_input("Medicamento")
    f3, f4 = st.columns(2)
    qtd = f3.number_input("Qtd", min_value=1, value=1)
    un = f4.selectbox("Tipo", ["Cx", "Fr", "Un"])
    inst = st.text_area("Instruções")
    if st.form_submit_button("➕ Adicionar Medicamento"):
        if med and inst:
            st.session_state.lista_meds.append({"n": med, "q": qtd, "u": un, "v": via, "i": inst})
            st.rerun()

if st.session_state.lista_meds:
    st.write(f"📌 Itens na lista: {len(st.session_state.lista_meds)}")
    if st.button("🗑️ Limpar Tudo"):
        st.session_state.lista_meds = []
        st.rerun()

# --- 3. BOTÃO DE GERAR (SEMPRE VISÍVEL SE HOUVER MEDS) ---
st.write("---")
if st.session_state.lista_meds:
    if st.button("🚀 GERAR RECEITA (2 VIAS)"):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        
        # Desenhar as duas vias (Lado 0 e Lado 148.5)
        for ox in [0, 148.5]:
            # Cabeçalho
            pdf.set_font("Arial", 'B', 12)
            pdf.set_xy(ox + 10, 10)
            pdf.cell(130, 6, txt="Dr. Eliéser Ferreira Gobbe", ln=True, align='C')
            pdf.set_font("Arial", '', 9)
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, txt="Médico Veterinário - CRMV-SC 2754", ln=True, align='C')
            pdf.set_x(ox + 10)
            pdf.cell(130, 4, txt="Rua Isidoro Schilickmann, 93-Santa Augusta", ln=True, align='C')
            
            # Paciente
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_x(ox + 10)
            pdf.cell(0, 5, txt=f"Paciente: {paciente}", ln=True)
            pdf.set_x(ox + 10)
            pdf.cell(0, 5, txt=f"Proprietário: {proprietario}    Data: {data_hoje}", ln=True)
            
            # Prescrição
            pdf.ln(5)
            pdf.set_x(ox + 10)
            pdf.cell(0, 6, txt="PRESCRIÇÃO:", ln=True)
            for it in st.session_state.lista_meds:
                pdf.set_font("Arial", 'B', 9)
                pdf.set_x(ox + 10)
                pdf.cell(0, 5, txt=f"{it['n']} - {it['q']} {it['u']} ({it['v']})", ln=True)
                pdf.set_font("Arial", '', 9)
                pdf.set_x(ox + 10)
                pdf.multi_cell(125, 4, txt=f"Instruções: {it['i']}")
            
            # Rodapé Comprador (Fiel ao anexo)
            ry = 160
            pdf.set_xy(ox + 10, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(65, 4, txt="Identificação do Comprador", ln=True)
            pdf.set_font("Arial", '', 8)
            for lab in ["Nome:", "Org. Em:", "Ident.:", "End:", "Cidade:", "UF:", "Tel:"]:
                pdf.set_x(ox + 10)
                pdf.cell(65, 4, txt=lab, ln=True)
            
            # Fornecedor
            pdf.set_xy(ox + 80, ry)
            pdf.set_font("Arial", 'B', 8)
            pdf.cell(60, 4, txt="Identificação do Fornecedor", ln=True, align='R')
            pdf.set_xy(ox + 80, ry + 20)
            pdf.cell(60, 4, txt="Assinatura do Farmacêutico", ln=True, align='R')
            pdf.set_x(ox + 80)
            pdf.cell(60, 4, txt="Data: ____/____/____", ln=True, align='R')

        # Linha central de corte
        pdf.line(148.5, 5, 148.5, 205)
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button(label="📥 CLIQUE AQUI PARA BAIXAR PDF", data=pdf_out, file_name="receita.pdf", mime="application/pdf")
