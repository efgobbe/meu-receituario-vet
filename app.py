import streamlit as st
from fpdf import FPDF

# Título do Aplicativo
st.title("📋 Gerador de Receituário Técnico")

# Campos de preenchimento
nome_pet = st.text_input("Nome do Animal")
peso = st.number_input("Peso (kg)", min_value=0.1, step=0.1)
medicamento = st.text_input("Medicamento / Princípio Ativo")
dose_mg_kg = st.number_input("Dose desejada (mg/kg)", min_value=0.0)

# Cálculo Técnico Automático
dose_total = peso * dose_mg_kg

if dose_total > 0:
    st.info(f"Cálculo Técnico: O paciente deve receber {dose_total:.2f} mg no total.")

# Botão para gerar PDF
if st.button("Gerar PDF do Receituário"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="RECEITUÁRIO VETERINÁRIO TÉCNICO", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Paciente: {nome_pet} | Peso: {peso}kg", ln=True)
    pdf.cell(200, 10, txt=f"Medicamento: {medicamento}", ln=True)
    pdf.cell(200, 10, txt=f"Dose Calculada: {dose_total:.2f} mg", ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("Clique aqui para Baixar", data=pdf_output, file_name="receita.pdf")
