import pandas as pd
import streamlit as st
import openai

# === INTERFACE DO APP ===
st.set_page_config(page_title="Análise de Vendas com IA", layout="centered")
st.title("📊 Análise Inteligente de Vendas com ChatGPT (GPT-3.5)")
st.write("Envie um arquivo Excel com dados de vendas e metas por região para obter uma análise automatizada com IA.")

# === ENTRADA DA CHAVE DE API ===
api_key = st.text_input("🔑 Insira sua chave da API OpenAI:", type="password")

# === UPLOAD DO ARQUIVO ===
arquivo = st.file_uploader("📁 Envie a planilha Excel (.xlsx)", type=["xlsx"])

if api_key and arquivo:
    client = openai.OpenAI(api_key=api_key)
    df = pd.read_excel(arquivo)
    st.write("📄 Pré-visualização dos dados:", df.head())

    try:
        resumo = df.groupby("Região").agg(
            Total_Vendas=("Vendas", "sum"),
            Meta_Total=("Meta Região", "sum")
        ).reset_index()

        prompt = "Você é um analista de negócios com foco em vendas. Com base nos dados abaixo, escreva um resumo executivo destacando:\n"
        prompt += "- Regiões que bateram ou não bateram suas metas\n"
        prompt += "- Destaque para os melhores desempenhos\n\n"

        for _, row in resumo.iterrows():
            status = "ACIMA" if row["Total_Vendas"] >= row["Meta_Total"] else "ABAIXO"
            prompt += f"Região: {row['Região']} | Vendas: R$ {row['Total_Vendas']:,} | Meta: R$ {row['Meta_Total']:,} => {status} da meta\n"

        prompt += "\nEscreva esse resumo em tom profissional e direto."

        if st.button("🚀 Gerar Análise com IA"):
            with st.spinner("Analisando com IA..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um analista de BI especialista em vendas."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                resumo_ia = response.choices[0].message.content
                st.subheader("✅ Resumo Gerado pela IA")
                st.markdown(resumo_ia)

    except Exception as e:
        st.error(f"Erro na análise: {e}")
elif not api_key and arquivo:
    st.warning("⚠️ Por favor, insira sua chave da API para continuar.")
