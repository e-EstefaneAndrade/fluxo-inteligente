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
3. Treinamento e comparação de dois modelos Random Forest Regressor
4. Geração das previsões de saldo de caixa para os próximos 30 dias

### Desempenho dos modelos

| Modelo | MAE (R$) | RMSE (R$) | R² |
|---|---|---|---|
| Modelo A (com saldo anterior) | 626,60 | 843,96 | 0,9991 |
| Modelo B (sem saldo anterior) — **modelo final** | 756,18 | 999,91 | 0,9987 |

O Modelo B foi escolhido para produção por eliminar a dependência recursiva do saldo do dia anterior, evitando acúmulo de erro ao longo do horizonte de previsão de 30 dias.

## Tecnologias

Python · Pandas · Scikit-learn (Random Forest) · Streamlit · Plotly · Matplotlib

## Autoria

Desenvolvido por **Estefane Andrade** — Especialização em Ciência de Dados, UTFPR, 2026.
