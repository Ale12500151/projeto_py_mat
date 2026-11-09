# Mapa de calor do crescimento por UF
# Integrante 1
# A populacao de cada estado e a soma dos municipios da base tratada (crescimento_municipios.csv)

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from layout import cabecalho
from estatisticas import fmt
from secoes.crescimento import carregar


@st.cache_data
def carregar_mapa():
    with open("dados/brutos/brasil_uf.geojson", encoding="utf-8") as f:
        return json.load(f)


def mostrar(filtros, arquivo=None):
    cabecalho("Mapa do crescimento por estado", "Crescimento da população entre o Censo 2010 e o Censo 2022, por UF", "Integrante 1")

    mun = carregar(arquivo)
    serie = mun.groupby(["uf", "regiao"], as_index=False)[["pop_2010", "pop_2022"]].sum()
    serie["taxa_geometrica_anual"] = ((serie["pop_2022"] / serie["pop_2010"]) ** (1 / 12) - 1) * 100

    # ---- mapa
    indicador = st.selectbox("Indicador do mapa", ["Crescimento acumulado 2010-2022 (%)", "Taxa geométrica anual 2010-2022 (%)"])
    mapa_df = serie.rename(columns={"pop_2010": "p10", "pop_2022": "p22"})
    mapa_df["crescimento"] = (mapa_df["p22"] / mapa_df["p10"] - 1) * 100
    mapa_df = mapa_df[mapa_df["regiao"].isin(filtros["regioes"])]
    coluna = "crescimento" if indicador.startswith("Crescimento") else "taxa_geometrica_anual"

    fig_mapa = px.choropleth(
        mapa_df, geojson=carregar_mapa(), locations="uf", featureidkey="properties.sigla",
        color=coluna, color_continuous_scale="Tealgrn", hover_name="uf",
        hover_data={"p10": ":,", "p22": ":,", "crescimento": ":.2f", "uf": False},
        labels={"crescimento": "Crescimento (%)", "taxa_geometrica_anual": "Taxa anual (%)", "p10": "Pop. 2010", "p22": "Pop. 2022"},
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(height=550, margin=dict(l=0, r=0, t=0, b=0))
    c1, c2 = st.columns([3, 2])
    c1.plotly_chart(fig_mapa, width="stretch", theme=None)
    ranking = mapa_df.sort_values("crescimento", ascending=False)[["uf", "crescimento"]]
    ranking.columns = ["UF", "Crescimento 2010-2022 (%)"]
    c2.dataframe(ranking.round(2), hide_index=True, width="stretch", height=550)

    maior = mapa_df.sort_values("crescimento").iloc[-1]
    menor = mapa_df.sort_values("crescimento").iloc[0]
    st.markdown(f"O estado que mais cresceu foi **{maior['uf']} ({fmt(maior['crescimento'], 1)}%)** e o que menos cresceu foi "
                f"**{menor['uf']} ({fmt(menor['crescimento'], 1)}%)**. O Norte e o Centro-Oeste continuam puxando o crescimento, "
                "enquanto Sul e Sudeste crescem devagar e já envelhecem mais rápido.")

    st.caption("Soma dos 5.565 municípios que já existiam em 2010. Os 5 criados depois ficam de fora, para comparar sempre os mesmos municípios.")
