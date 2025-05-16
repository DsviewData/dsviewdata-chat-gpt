import pandas as pd
import streamlit as st

# === CONFIGURAÇÃO DO APP ===
st.set_page_config(page_title="Análise de Vendas com IA", layout="centered")
st.title("📊 DSViewData - Análise Inteligente de Vendas")
st.write("Envie sua planilha de vendas e receba uma análise automática com IA (simulado para MVP).")

# === LINK PARA PLANILHA MODELO ===
with st.expander("📁 Baixe o modelo de planilha para envio"):
    st.markdown("[Clique aqui para baixar](https://dsviewdata.com/modelo_vendas.xlsx)")

# === UPLOAD DA PLANILHA ===
arquivo = st.file_uploader("Envie sua planilha preenchida (.xlsx)", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    colunas_esperadas = ["Data", "Região", "Produto", "Vendedor", "Vendas", "Meta Região"]

    if not all(col in df.columns for col in colunas_esperadas):
        st.error("❌ A planilha está com colunas incorretas. Baixe o modelo e siga o formato padrão.")
    else:
        st.success("✅ Planilha recebida com sucesso.")
        st.write("📊 Pré-visualização dos dados:", df.head())

        resumo = df.groupby("Região").agg(
            Total_Vendas=("Vendas", "sum"),
            Meta_Total=("Meta Região", "sum")
        ).reset_index()

        st.subheader("📈 Total por Região")
        st.dataframe(resumo)

        if st.button("🚀 Gerar Análise Simulada"):
            st.subheader("✅ Análise Inteligente (Simulada)")
            st.markdown(
                "A região Sul superou as metas com folga, seguida por Centro-Oeste. "
                "Nordeste e Sudeste ficaram abaixo das metas e requerem ações de reforço. "
                "Sugerimos campanhas regionais e foco nos produtos de maior ticket médio."
            )
