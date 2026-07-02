# ☕ Fluxo Inteligente

Sistema de Inteligência Financeira para Pequenas Cafeterias — Trabalho de Conclusão de Curso da Especialização em Ciência de Dados (UTFPR).

**Dashboard online:** https://fluxo-inteligente-8yr7hfrywdgxhwappwvehgi.streamlit.app/

## Sobre o projeto

O Fluxo Inteligente é um protótipo SaaS que utiliza Ciência de Dados e Machine Learning para projetar o saldo de caixa futuro de pequenas cafeterias, identificar os fatores que mais impactam o caixa e gerar recomendações gerenciais automatizadas.

**Principais funcionalidades:**
- Monitoramento financeiro (receita, saldo, fluxo de caixa)
- Projeção do saldo de caixa para os próximos 30 dias (Random Forest)
- Identificação dos fatores que mais impactam o caixa
- Recomendações gerenciais e alertas automáticos

## Estrutura do repositório

```
fluxo-inteligente/
├── app.py                     # Dashboard Streamlit
├── notebooks/
│   └── fluxo_inteligente.ipynb  # Pipeline completo: dados, features, modelo, previsão
├── dados/
│   ├── dataset_financeiro_fluxo_inteligente.csv
│   ├── previsao_30_dias_fluxo_inteligente.csv
│   ├── importancia_variaveis.csv
│   └── historico_previsao_fluxo_inteligente.csv
├── requirements.txt
└── README.md
```

## Como executar localmente

```bash
git clone https://github.com/e-EstefaneAndrade/fluxo-inteligente.git
cd fluxo-inteligente
pip install -r requirements.txt
streamlit run app.py
```

## Pipeline de dados e modelagem

O notebook realiza todo o processo:
1. Tratamento da base [Coffee Shop Sales](https://www.kaggle.com/datasets/keremkarayaz/coffee-shop-sales) e construção do modelo financeiro (receita, CMV, folha, taxas, custos fixos e saldo acumulado)
2. Análise exploratória e engenharia de atributos (variáveis de calendário, defasagens e médias móveis de 7/30 dias)
3. Treinamento e comparação de modelos (Random Forest e modelos de tendência/drift), com validação cronológica
4. Geração das previsões de saldo de caixa para os próximos 30 dias com o modelo final (drift)

### Desempenho dos modelos (validação cronológica)

| Modelo | MAE (R$) | RMSE (R$) | R² |
|---|---|---|---|
| Persistência (flat) | 13.800,99 | 15.987,18 | -2,9248 |
| Drift (média de fluxo, 7 dias) | 1.834,70 | 2.310,27 | 0,9180 |
| **Drift (média de fluxo, 30 dias) — modelo final** | **1.183,28** | **1.556,87** | **0,9628** |
| Modelo A (Random Forest) | 16.424,39 | 18.518,05 | -4,2657 |
| Modelo B (Random Forest) | 16.795,03 | 18.831,55 | -4,4455 |

Os dois modelos de Random Forest, apesar de amplamente usados em problemas de regressão, não conseguem extrapolar além do intervalo de valores vistos no treinamento — uma limitação estrutural para prever uma série cumulativa e crescente como o saldo de caixa. O modelo final adotado é um modelo de tendência (**drift**), que projeta a taxa de variação recente do fluxo de caixa para os dias seguintes, e superou com folga tanto o Random Forest quanto a persistência simples.

## Tecnologias

Python · Pandas · Scikit-learn (Random Forest) · Streamlit · Plotly · Matplotlib

## Autoria

Desenvolvido por **Estefane Andrade** — Especialização em Ciência de Dados, UTFPR, 2026.
