import streamlit as st
from layout import cabecalho


def mostrar(filtros, arquivo=None):
    cabecalho("Quanto cada cidade cresceu?", "Crescimento da população dos municípios entre o Censo 2010 e o Censo 2022", "Projeto Integrador • Números que Falam • Integrante 1")
    st.markdown(
        "Somos a **Radar Urbano**, uma startup de análise de dados contratada pelos prefeitos de Curitiba, "
        "Porto Alegre, Belo Horizonte, Salvador e Florianópolis para ajudar na revisão dos **Planos Diretores**."
    )

    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Pergunta que esta parte responde")
        st.markdown("**Qual é a taxa média de crescimento populacional acumulada por cidade?**")
        st.subheader("O que tem aqui")
        st.markdown("""- **Crescimento dos municípios:** KPIs, estatísticas (média, mediana, moda, quartis, IQR, amplitude, desvio padrão), histograma e as capitais do cenário
- **Mapa por estado:** mapa de calor do crescimento de cada UF""")
    with c2:
        st.subheader("Nossos clientes")
        st.markdown(
            """
| Persona | Cargo |
|---|---|
| Carlos | Prefeito de Curitiba (PR) |
| Eduardo | Prefeito de Porto Alegre (RS) |
| Elisa | Prefeita de Belo Horizonte (MG) |
| Jorge | Prefeito de Salvador (BA) |
| Roberto | Prefeito de Florianópolis (SC) |
"""
        )
        st.info("Use o menu da barra lateral para navegar. Os filtros valem para todas as telas desta parte.")

    st.subheader("De onde vêm os dados")
    st.markdown("""- **Tabela 4709 (SIDRA):** nome e população dos municípios no Censo 2022
- **Censo 2010 x 2022 por município:** população dos 5.565 municípios que já existiam em 2010
- Os 5 municípios criados depois de 2010 não entram no cálculo (não existiam no Censo 2010)""")
