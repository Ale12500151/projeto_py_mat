# Funcoes de estatistica que o grupo usa nas secoes
# (comecou na parte do Integrante 1 e depois a gente passou pra ca pra todo mundo usar)

import numpy as np
import pandas as pd


def classe_modal(valores, largura=5):
    # para variavel continua (ex: crescimento em %) quase nenhum valor se repete,
    # entao a moda e calculada pela classe (intervalo) que tem mais municipios
    valores = pd.Series(valores).dropna()
    inicio = np.floor(valores.min() / largura) * largura
    fim = np.ceil(valores.max() / largura) * largura + largura
    bordas = np.arange(inicio, fim, largura)
    contagem = pd.cut(valores, bins=bordas, right=False).value_counts()
    classe = contagem.idxmax()
    return classe.left, classe.right, int(contagem.max())


def calcular_estatisticas(valores, largura_moda=5):
    s = pd.Series(valores).dropna()
    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    moda_ini, moda_fim, moda_qtd = classe_modal(s, largura_moda)

    resultado = {
        "n": len(s),
        "media": s.mean(),
        "mediana": s.median(),
        "moda_ini": moda_ini,
        "moda_fim": moda_fim,
        "moda_qtd": moda_qtd,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "minimo": s.min(),
        "maximo": s.max(),
        "amplitude": s.max() - s.min(),
        "variancia": s.var(ddof=1),       # amostral (n-1), igual o pandas faz por padrao
        "desvio_padrao": s.std(ddof=1),
        "lim_inferior": q1 - 1.5 * iqr,
        "lim_superior": q3 + 1.5 * iqr,
    }
    resultado["cv"] = resultado["desvio_padrao"] / abs(resultado["media"]) * 100 if resultado["media"] != 0 else np.nan
    return resultado


def tabela_estatisticas(est, unidade="%"):
    # monta um dataframe bonitinho pra mostrar no streamlit
    linhas = [
        ["Média", est["media"]],
        ["Mediana (Q2)", est["mediana"]],
        ["Moda (classe modal)", f'{est["moda_ini"]:.0f} a {est["moda_fim"]:.0f}{unidade} ({est["moda_qtd"]} municípios)'],
        ["Q1 (25%)", est["q1"]],
        ["Q3 (75%)", est["q3"]],
        ["IQR (Q3 - Q1)", est["iqr"]],
        ["Mínimo", est["minimo"]],
        ["Máximo", est["maximo"]],
        ["Amplitude", est["amplitude"]],
        ["Variância", est["variancia"]],
        ["Desvio padrão", est["desvio_padrao"]],
        ["Coef. de variação", f'{est["cv"]:.1f}%'],
        ["Limite inferior (Q1 - 1,5·IQR)", est["lim_inferior"]],
        ["Limite superior (Q3 + 1,5·IQR)", est["lim_superior"]],
    ]
    tabela = pd.DataFrame(linhas, columns=["Medida", "Valor"])
    tabela["Valor"] = tabela["Valor"].apply(lambda v: f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(v, (int, float, np.floating)) else v)
    return tabela


def ler_arquivo(arquivo):
    # aceita csv (com , ou ;) e xlsx vindo do st.file_uploader
    nome = arquivo.name.lower()
    if nome.endswith(".xlsx") or nome.endswith(".xls"):
        return pd.read_excel(arquivo)
    return pd.read_csv(arquivo, sep=None, engine="python", encoding="utf-8-sig")


def fmt(numero, casas=0):
    # formato brasileiro: 1.234.567,89
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
