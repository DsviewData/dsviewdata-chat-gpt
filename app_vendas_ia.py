import pandas as pd
import streamlit as st

# === INTERFACE DO APP ===
st.set_page_config(page_title="Análise Simulada com IA", layout="centered")
st.title("📊 Análise Inteligente de Vendas (Simulado)")
st.write("Envie um arquivo Excel com dados de vendas e metas por região. A resposta da IA será simulada para fins de teste.")

# === UPLOAD DO ARQUIVO ===
arquivo = st.file_uploader("📁 Envie a planilha Excel (.xlsx)", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.write("📄 Pré-visualização dos dados:", df.head())

    try:
        resumo = df.groupby("Região").agg(
            Total_Vendas=("Vendas", "sum"),
            Meta_Total=("Meta Região", "sum")
        ).reset_index()

        # Exibe o resumo numérico
        st.subheader("📊 Total por Região")
        st.dataframe(resumo)

        if st.button("🚀 Gerar Análise Simulada"):
            st.subheader("✅ Resumo Gerado (Simulado)")
            texto = (
                "A região Sul apresentou o melhor desempenho, superando a meta com um total acumulado de R$ 51.500. "
                "O Centro-Oeste também atingiu sua meta. Já as regiões Nordeste e Sudeste ficaram abaixo do esperado, "
                "com diferenças de R$ 7.500 e R$ 5.500, respectivamente. Recomendam-se ações de reforço nessas regiões para os próximos ciclos."
            )
            st.markdown(texto)

    except Exception as e:
        st.error(f"Erro na análise: {e}")
