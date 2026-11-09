# ETL - Crescimento populacional dos municipios (Censo 2010 x Censo 2022)
# Integrante 1
#
# Bases usadas (IBGE / SIDRA):
#   - tabela4709_municipios.csv  -> codigo, nome do municipio e populacao 2022
#   - censo_populacao_municipios_2010_2022.csv -> populacao 2010 e 2022 por codigo
#
# Rodar a partir da pasta do projeto:  python etl/tratar_crescimento.py

import pandas as pd
import numpy as np

PASTA_BRUTOS = "dados/brutos/"
PASTA_TRATADOS = "dados/tratados/"

# codigo IBGE das 27 capitais
CAPITAIS = [1100205, 1200401, 1302603, 1400100, 1501402, 1600303, 1721000,
            2111300, 2211001, 2304400, 2408102, 2507507, 2611606, 2704302,
            2800308, 2927408, 3106200, 3205309, 3304557, 3550308, 4106902,
            4205407, 4314902, 5002704, 5103403, 5208707, 5300108]

REGIOES = {1: "Norte", 2: "Nordeste", 3: "Sudeste", 4: "Sul", 5: "Centro-Oeste"}


def porte(pop):
    # faixas de porte parecidas com as que o IBGE usa nas publicacoes
    if pop <= 20000:
        return "Pequeno (até 20 mil)"
    elif pop <= 100000:
        return "Médio (20 a 100 mil)"
    elif pop <= 500000:
        return "Grande (100 a 500 mil)"
    else:
        return "Metrópole (mais de 500 mil)"


def tratar():
    nomes = pd.read_csv(PASTA_BRUTOS + "tabela4709_municipios.csv", encoding="utf-8-sig")
    censos = pd.read_csv(PASTA_BRUTOS + "censo_populacao_municipios_2010_2022.csv", sep=";")

    print("linhas tabela 4709:", len(nomes))
    print("linhas censos:", len(censos))

    nomes.columns = ["cod_mun", "municipio_uf", "pop_2022_4709"]

    # o nome vem junto com a UF, ex: "Curitiba (PR)"
    nomes["municipio"] = nomes["municipio_uf"].str.replace(r"\s*\([A-Z]{2}\)$", "", regex=True)
    nomes["uf"] = nomes["municipio_uf"].str.extract(r"\(([A-Z]{2})\)$")[0]

    df = nomes.merge(censos, on="cod_mun", how="left")

    # conferencia: a populacao 2022 das duas bases tem que bater
    diferentes = df[(df["pop_2022"].notna()) & (df["pop_2022"] != df["pop_2022_4709"])]
    print("municipios com 2022 diferente entre as bases:", len(diferentes))

    # 5 municipios foram criados depois de 2010 (ex: Pescaria Brava/SC, Mojuí dos Campos/PA)
    # nao da pra calcular crescimento deles, entao saem da analise
    sem_2010 = df[df["pop_2010"].isna()]
    print("municipios sem populacao em 2010 (removidos):")
    print(sem_2010[["municipio_uf", "pop_2022_4709"]].to_string(index=False))
    df = df.dropna(subset=["pop_2010"])

    df["pop_2010"] = df["pop_2010"].astype(int)
    df["pop_2022"] = df["pop_2022"].astype(int)

    df["cod_uf"] = df["cod_mun"] // 100000
    df["regiao"] = (df["cod_uf"] // 10).map(REGIOES)
    df["capital"] = df["cod_mun"].isin(CAPITAIS)
    df["porte"] = df["pop_2022"].apply(porte)

    # crescimento acumulado em 12 anos (%)
    df["variacao_absoluta"] = df["pop_2022"] - df["pop_2010"]
    df["crescimento_acumulado"] = (df["pop_2022"] / df["pop_2010"] - 1) * 100

    # taxa geometrica media anual, mesma formula do IBGE: (P2022/P2010)^(1/12) - 1
    df["taxa_geometrica_anual"] = ((df["pop_2022"] / df["pop_2010"]) ** (1 / 12) - 1) * 100

    df["crescimento_acumulado"] = df["crescimento_acumulado"].round(2)
    df["taxa_geometrica_anual"] = df["taxa_geometrica_anual"].round(3)

    colunas = ["cod_mun", "municipio", "uf", "regiao", "capital", "porte",
               "pop_2010", "pop_2022", "variacao_absoluta",
               "crescimento_acumulado", "taxa_geometrica_anual"]
    df = df[colunas].sort_values("cod_mun")

    df.to_csv(PASTA_TRATADOS + "crescimento_municipios.csv", index=False, encoding="utf-8")
    print("arquivo salvo com", len(df), "municipios")
    print("Brasil 2010:", df["pop_2010"].sum(), "| Brasil 2022 (sem os 5 novos):", df["pop_2022"].sum())
    return df


if __name__ == "__main__":
    tratar()
