# Parte visual do app (cores, css e cabecalho das telas)
# Feito pelo grupo na integracao, para todas as secoes ficarem com a mesma cara

import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go

# paleta da Radar Urbano
VERDE = "#0F766E"
VERDE_CLARO = "#5EEAD4"
AZUL = "#155E75"
LARANJA = "#F59E0B"
VERMELHO = "#DC2626"
CINZA = "#94A3B8"
TEXTO = "#1E293B"

CORES = [VERDE, LARANJA, AZUL, "#E11D48", "#7C3AED", "#65A30D", "#0EA5E9", "#A16207"]


def configurar_graficos():
    pio.templates["radar"] = go.layout.Template(
        layout=dict(
            colorway=CORES,
            font=dict(family="Source Sans Pro, Arial, sans-serif", color=TEXTO, size=13),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            yaxis=dict(gridcolor="#E2E8F0", zerolinecolor="#CBD5E1"),
            hoverlabel=dict(bgcolor="white", font_size=13),
            margin=dict(t=40),
        )
    )
    pio.templates.default = "plotly_white+radar"


CSS = """
<style>
#MainMenu, footer, [data-testid="stAppDeployButton"], [data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1.5rem; max-width: 1350px;}

/* barra lateral */
[data-testid="stSidebar"] {background: #EEF5F4; border-right: 1px solid #D5E5E2;}
[data-testid="stSidebar"] h3 {font-size: 0.95rem; text-transform: uppercase; letter-spacing: .06em; color: #0F766E;}

/* cabecalho das telas */
.cabecalho {
    background: linear-gradient(110deg, #0F766E 0%, #155E75 100%);
    color: white; padding: 26px 30px; border-radius: 16px; margin-bottom: 22px;
}
.cabecalho .etiqueta {
    display: inline-block; background: rgba(255,255,255,.18); padding: 3px 12px;
    border-radius: 20px; font-size: .8rem; margin-bottom: 8px;
}
.cabecalho h1 {color: white; font-size: 2rem; margin: 0; padding: 0;}
.cabecalho p {color: #D1FAE5; margin: 6px 0 0 0; font-size: 1rem;}

/* subtitulos com barrinha */
.block-container h3 {border-left: 5px solid #F59E0B; padding-left: 10px; margin-top: 1.2rem;}

/* cards dos KPIs */
[data-testid="stMetric"] {
    background: white; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 14px 18px; box-shadow: 0 1px 3px rgba(15, 23, 42, .06);
    border-top: 4px solid #0F766E;
}
[data-testid="stMetricLabel"] p {font-size: .85rem; color: #475569;}
[data-testid="stMetricValue"] {font-size: 1.65rem; color: #0F172A;}

/* graficos e tabelas em "caixinhas" */
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
    background: white; border-radius: 14px; border: 1px solid #E2E8F0; padding: 6px;
}
</style>
"""


def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)


def cabecalho(titulo, descricao, etiqueta=""):
    html = '<div class="cabecalho">'
    if etiqueta:
        html += f'<span class="etiqueta">{etiqueta}</span>'
    html += f"<h1>{titulo}</h1><p>{descricao}</p></div>"
    st.markdown(html, unsafe_allow_html=True)
