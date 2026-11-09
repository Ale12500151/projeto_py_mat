import streamlit as st

from secoes import inicio, crescimento, mapa
from layout import aplicar_estilo, configurar_graficos

st.set_page_config(page_title="Radar Urbano | Crescimento dos municípios", page_icon="📊", layout="wide")
aplicar_estilo()
configurar_graficos()

REGIOES_UF = {
    "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
    "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
    "Sudeste": ["ES", "MG", "RJ", "SP"],
    "Sul": ["PR", "RS", "SC"],
    "Centro-Oeste": ["DF", "GO", "MS", "MT"],
}
# estados dos prefeitos do cenario (Curitiba, Porto Alegre, BH, Salvador, Florianopolis)
UFS_PERSONAS = ["BA", "MG", "PR", "RS", "SC"]
FAIXAS = [f"{i}-{i + 4}" for i in range(0, 100, 5)] + ["100+"]

PAGINAS = {
    "Início": inicio,
    "Crescimento dos municípios": crescimento,
    "Mapa por estado": mapa,
}
ICONES = {
    "Início": ":material/home:",
    "Crescimento dos municípios": ":material/trending_up:",
    "Mapa por estado": ":material/map:",
}

# ---------------- barra lateral ----------------
st.sidebar.image("imagens/logo.png", width="stretch")
st.sidebar.caption("Indicador 3: Crescimento Demográfico • Parte do Integrante 1")

st.sidebar.subheader("Navegação")
pagina = st.sidebar.radio("Navegação", list(PAGINAS.keys()), format_func=lambda p: f"{ICONES[p]} {p}",
                          label_visibility="collapsed")

st.sidebar.divider()
st.sidebar.subheader("Filtros")

regioes = st.sidebar.multiselect("Região", list(REGIOES_UF.keys()), default=list(REGIOES_UF.keys()))
if not regioes:
    regioes = list(REGIOES_UF.keys())

opcoes_uf = sorted([uf for r in regioes for uf in REGIOES_UF[r]])
padrao_uf = [uf for uf in UFS_PERSONAS if uf in opcoes_uf]
ufs = st.sidebar.multiselect("Unidade da Federação", opcoes_uf, default=padrao_uf,
                             help="Vem marcado com os estados das capitais do cenário. Deixe vazio para usar todas as UFs das regiões escolhidas.")
if not ufs:
    ufs = opcoes_uf

filtros = {"regioes": regioes, "ufs": ufs}

portes = st.sidebar.multiselect(
    "Porte do município",
    ["Pequeno (até 20 mil)", "Médio (20 a 100 mil)", "Grande (100 a 500 mil)", "Metrópole (mais de 500 mil)"],
    default=["Pequeno (até 20 mil)", "Médio (20 a 100 mil)", "Grande (100 a 500 mil)", "Metrópole (mais de 500 mil)"],
)
filtros["portes"] = portes

# upload da base da pagina atual (opcional)
arquivo = None
modulo = PAGINAS[pagina]
if hasattr(modulo, "COLUNAS_UPLOAD"):
    st.sidebar.divider()
    st.sidebar.subheader("Upload de dados")
    arquivo = st.sidebar.file_uploader(
        "Enviar base desta tela (CSV ou XLSX)", type=["csv", "xlsx"], key="upload_" + pagina
    )
    st.sidebar.caption("Colunas esperadas: " + ", ".join(modulo.COLUNAS_UPLOAD))
    st.sidebar.caption("Sem upload, o app usa a base do IBGE que já está na pasta dados/tratados.")

st.sidebar.divider()
st.sidebar.caption("Fonte: IBGE, Censos Demográficos 2010 e 2022 (SIDRA)")

# ---------------- conteudo ----------------
modulo.mostrar(filtros, arquivo)
