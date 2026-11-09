# Secao 1 - Crescimento populacional dos municipios (2010 x 2022)
# Integrante 1

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from layout import cabecalho, VERDE, VERMELHO, LARANJA
from estatisticas import calcular_estatisticas, tabela_estatisticas, ler_arquivo, fmt

COLUNAS_UPLOAD = ["municipio", "uf", "regiao", "capital", "porte", "pop_2010", "pop_2022"]
CAPITAIS_CENARIO = {
    "Curitiba": "PR", "Porto Alegre": "RS", "Belo Horizonte": "MG",
    "Salvador": "BA", "Florianópolis": "SC",
}


@st.cache_data
def carregar_padrao():
    return pd.read_csv("dados/tratados/crescimento_municipios.csv")


def preparar_upload(arquivo):
    df = ler_arquivo(arquivo)
    faltando = [c for c in COLUNAS_UPLOAD if c not in df.columns]
    if faltando:
        st.error(f"O arquivo enviado não tem as colunas: {', '.join(faltando)}. Usando a base padrão.")
        return None
    df = df.dropna(subset=["pop_2010", "pop_2022"])
    df = df[df["pop_2010"] > 0]
    # recalcula as taxas para nao depender do que veio no arquivo
    df["variacao_absoluta"] = df["pop_2022"] - df["pop_2010"]
    df["crescimento_acumulado"] = (df["pop_2022"] / df["pop_2010"] - 1) * 100
    df["taxa_geometrica_anual"] = ((df["pop_2022"] / df["pop_2010"]) ** (1 / 12) - 1) * 100
    df["capital"] = df["capital"].astype(str).str.lower().isin(["true", "1", "sim"])
    st.success(f"Base enviada carregada: {len(df)} municípios.")
    return df


def carregar(arquivo=None):
    if arquivo is not None:
        df = preparar_upload(arquivo)
        if df is not None:
            return df
    return carregar_padrao()


def aplicar_filtros(df, filtros):
    df = df[df["regiao"].isin(filtros["regioes"])]
    df = df[df["uf"].isin(filtros["ufs"])]
    df = df[df["porte"].isin(filtros["portes"])]
    return df


def mostrar(filtros, arquivo=None):
    cabecalho("Crescimento populacional dos municípios", "Comparação entre o Censo 2010 e o Censo 2022", "Integrante 1")

    base = carregar(arquivo)
    df = aplicar_filtros(base, filtros)

    if df.empty:
        st.warning("Nenhum município com esses filtros.")
        return

    est = calcular_estatisticas(df["crescimento_acumulado"])
    pop10 = df["pop_2010"].sum()
    pop22 = df["pop_2022"].sum()
    cresc_total = (pop22 / pop10 - 1) * 100
    perderam = (df["crescimento_acumulado"] < 0).sum()

    # ---- KPIs
    k1, k2, k3, k4, k6, k5 = st.columns(6)
    k1.metric("Municípios", fmt(len(df)))
    k2.metric("População 2022", fmt(pop22), f"{fmt(cresc_total, 2)}% desde 2010")
    k3.metric("Média por cidade", f"{fmt(est['media'], 2)}%")
    k4.metric("Mediana por cidade", f"{fmt(est['mediana'], 2)}%")
    k6.metric("IQR", f"{fmt(est['iqr'], 2)} p.p.")
    k5.metric("Perderam população", fmt(perderam), f"{fmt(perderam / len(df) * 100, 1)}% do total", delta_color="off")

    st.markdown(
        f"Nos estados selecionados ({', '.join(filtros['ufs'])}), um município **cresceu em média "
        f"{fmt(est['media'], 2)}%** entre 2010 e 2022, o que dá uma taxa geométrica média de "
        f"**{fmt(df['taxa_geometrica_anual'].mean(), 2)}% ao ano**. Mas metade das cidades cresceu menos de "
        f"**{fmt(est['mediana'], 2)}%** (mediana)."
    )

    # ---- capitais do cenario
    st.subheader("As capitais dos nossos clientes")
    caps = base[base["capital"] & base["municipio"].isin(CAPITAIS_CENARIO.keys())].copy()
    caps = caps.sort_values("crescimento_acumulado")
    if caps.empty:
        st.info("A base enviada não tem as capitais do cenário.")
        caps = carregar_padrao()
        caps = caps[caps["capital"] & caps["municipio"].isin(CAPITAIS_CENARIO.keys())].sort_values("crescimento_acumulado")
    cores = [VERMELHO if v < 0 else VERDE for v in caps["crescimento_acumulado"]]
    fig_cap = go.Figure(go.Bar(
        x=caps["crescimento_acumulado"], y=caps["municipio"], orientation="h",
        marker_color=cores, text=[f"{v:.1f}%".replace(".", ",") for v in caps["crescimento_acumulado"]],
        textposition="outside",
        customdata=caps[["pop_2010", "pop_2022"]],
        hovertemplate="%{y}<br>2010: %{customdata[0]:,}<br>2022: %{customdata[1]:,}<br>Crescimento: %{x:.2f}%<extra></extra>",
    ))
    fig_cap.update_layout(xaxis_title="Crescimento acumulado 2010-2022 (%)", yaxis_title="",
                          xaxis_range=[min(caps["crescimento_acumulado"].min() * 1.6, -5), max(caps["crescimento_acumulado"].max() * 1.25, 5)],
                          height=320, margin=dict(l=10, r=40, t=10, b=40))
    fig_cap.add_vline(x=0, line_color="gray")

    c1, c2 = st.columns([3, 2])
    c1.plotly_chart(fig_cap, width="stretch", theme=None)
    tab_caps = caps[["municipio", "pop_2010", "pop_2022", "crescimento_acumulado"]].copy()
    tab_caps.columns = ["Capital", "Pop. 2010", "Pop. 2022", "Cresc. (%)"]
    tab_caps["Pop. 2010"] = tab_caps["Pop. 2010"].apply(fmt)
    tab_caps["Pop. 2022"] = tab_caps["Pop. 2022"].apply(fmt)
    tab_caps["Cresc. (%)"] = tab_caps["Cresc. (%)"].round(2)
    c2.dataframe(tab_caps, hide_index=True, width="stretch")
    encolheram = caps[caps["crescimento_acumulado"] < 0]["municipio"].tolist()
    mais = caps.iloc[-1]["municipio"]
    if encolheram:
        c2.caption(f"Perderam moradores: {', '.join(encolheram)}. Quem mais cresceu foi {mais}.")


    # ---- estatisticas
    st.subheader("Estatísticas do crescimento acumulado (%)")
    c1, c2 = st.columns([2, 3])
    with c1:
        st.dataframe(tabela_estatisticas(est), hide_index=True, width="stretch", height=530)
    with c2:
        fig_hist = px.histogram(df, x="crescimento_acumulado", nbins=60,
                                labels={"crescimento_acumulado": "Crescimento acumulado 2010-2022 (%)"},
                                color_discrete_sequence=[VERDE])
        # linhas da media e mediana (o texto fica na legenda pra nao ficar em cima do grafico)
        fig_hist.add_vline(x=est["media"], line_dash="dash", line_color=VERMELHO, line_width=2.5)
        fig_hist.add_vline(x=est["mediana"], line_dash="dot", line_color=LARANJA, line_width=2.5)
        fig_hist.add_scatter(x=[None], y=[None], mode="lines", name=f"Média: {fmt(est['media'], 2)}%",
                             line=dict(color=VERMELHO, dash="dash", width=2.5))
        fig_hist.add_scatter(x=[None], y=[None], mode="lines", name=f"Mediana: {fmt(est['mediana'], 2)}%",
                             line=dict(color=LARANJA, dash="dot", width=2.5))
        fig_hist.update_layout(legend=dict(orientation="h", y=1.08, x=0))
        fig_hist.update_layout(yaxis_title="Quantidade de municípios", height=530, bargap=0.05)
        st.plotly_chart(fig_hist, width="stretch", theme=None)

    if est["media"] > est["mediana"]:
        leitura = ("A **média é maior que a mediana**, então a distribuição tem **assimetria à direita**: "
                   "poucas cidades que cresceram muito puxam a média para cima.")
    else:
        leitura = ("A **média é menor que a mediana**, então a distribuição tem **assimetria à esquerda**: "
                   "as cidades que encolheram muito puxam a média para baixo.")
    st.markdown(
        f"{leitura} O desvio padrão de **{fmt(est['desvio_padrao'], 2)} pontos percentuais** e a amplitude de "
        f"**{fmt(est['amplitude'], 2)} p.p.** mostram que os municípios são bem diferentes entre si. "
        f"Por isso, para o planejamento, a **mediana** é a referência mais segura do que é um crescimento 'típico'."
    )

    # ---- comparacao por UF
    st.subheader("Média x mediana por estado")
    por_uf = df.groupby("uf").agg(
        media=("crescimento_acumulado", "mean"),
        mediana=("crescimento_acumulado", "median"),
        desvio=("crescimento_acumulado", "std"),
        municipios=("municipio", "count"),
        pop_2010=("pop_2010", "sum"),
        pop_2022=("pop_2022", "sum"),
    ).reset_index()
    por_uf["crescimento_estado"] = (por_uf["pop_2022"] / por_uf["pop_2010"] - 1) * 100
    longo = por_uf.melt(id_vars="uf", value_vars=["media", "mediana", "crescimento_estado"],
                        var_name="medida", value_name="valor")
    longo["medida"] = longo["medida"].map({"media": "Média dos municípios", "mediana": "Mediana dos municípios",
                                           "crescimento_estado": "Crescimento do estado (total)"})
    fig_uf = px.bar(longo, x="uf", y="valor", color="medida", barmode="group",
                    labels={"uf": "UF", "valor": "Crescimento 2010-2022 (%)", "medida": ""})
    fig_uf.update_layout(height=420, legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_uf, width="stretch", theme=None)
    st.caption("O crescimento do estado (total) é diferente da média dos municípios: no total, as cidades grandes pesam mais.")

    with st.expander("Ver tabela dos municípios filtrados"):
        st.dataframe(df.sort_values("crescimento_acumulado", ascending=False), hide_index=True, width="stretch")
        st.download_button("Baixar CSV tratado", df.to_csv(index=False).encode("utf-8"),
                           "crescimento_municipios_filtrado.csv", "text/csv")
