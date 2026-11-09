# Parte 1: Crescimento dos municípios e mapa

Projeto Integrador Python e Matemática, **Indicador 3: População e Crescimento Demográfico**.
Parte individual do **Integrante 1** no painel da startup **Radar Urbano**.

**Pergunta de negócio:** qual é a taxa média de crescimento populacional acumulada por cidade?

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O mapa precisa de internet para desenhar o contorno dos estados.

Para refazer a base tratada a partir dos arquivos do IBGE:

```bash
python etl/tratar_crescimento.py
```

## Arquivos

| Arquivo | O que faz |
|---|---|
| `app.py` | Menu lateral, filtros (Região, UF, Porte) e upload |
| `etl/tratar_crescimento.py` | ETL: junta Censo 2010 e 2022, limpa e calcula as taxas |
| `estatisticas.py` | Média, mediana, moda, quartis, IQR, amplitude, variância, desvio padrão |
| `secoes/crescimento.py` | Tela de crescimento: KPIs, estatísticas, histograma, capitais e comparação por UF |
| `secoes/mapa.py` | Mapa de calor (coroplético) do crescimento por UF |
| `dados/brutos/` | Arquivos do IBGE como vieram |
| `dados/tratados/crescimento_municipios.csv` | Base tratada |
| `ANALISE.md` | Análise descritiva |

## Fórmulas

- Crescimento acumulado (%) = (Pop 2022 / Pop 2010 - 1) × 100
- Taxa geométrica anual (%) = ((Pop 2022 / Pop 2010)^(1/12) - 1) × 100
- IQR = Q3 - Q1

Fonte: IBGE, Censos Demográficos 2010 e 2022 (SIDRA, tabela 4709).
