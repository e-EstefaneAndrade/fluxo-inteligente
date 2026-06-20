import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# FORMATAÇÃO BRASILEIRA
# =====================================

def moeda_br(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="Fluxo Inteligente",
    page_icon="☕",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("☕ Fluxo Inteligente")

    st.markdown(
        """
        **Sistema de Inteligência Financeira
        para Pequenas Cafeterias**

        ---

        Projeto de Especialização

        Ciência de Dados

        ---

        Desenvolvido por Estefane Andrade
        """
    )

# =====================================
# CARREGAMENTO DOS DADOS
# =====================================

df_financeiro = pd.read_csv(
    "dados/dataset_financeiro_fluxo_inteligente.csv"
)

df_previsao = pd.read_csv(
    "dados/previsao_30_dias_fluxo_inteligente.csv"
)

df_importancia = pd.read_csv(
    "dados/importancia_variaveis.csv"
)

# =====================================
# TÍTULO
# =====================================

st.title("☕ Fluxo Inteligente")

st.subheader(
    "Sistema de Inteligência Financeira para Pequenas Cafeterias"
)

st.info(
    """
    O Fluxo Inteligente é uma plataforma de apoio à decisão para pequenas cafeterias.

    Utilizando técnicas de Ciência de Dados e Machine Learning, o sistema projeta o saldo de caixa futuro e gera insights financeiros para auxiliar a gestão do negócio.
    """
)

# =====================================
# INDICADORES
# =====================================

receita_total = df_financeiro["receita_dia"].sum()

saldo_atual = df_financeiro["saldo_caixa"].iloc[-1]

saldo_previsto = df_previsao["saldo_previsto"].iloc[-1]

crescimento = (
    (saldo_previsto - saldo_atual)
    / saldo_atual
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📈 Receita Total",
    moeda_br(receita_total)
)

col2.metric(
    "💰 Saldo Atual",
    moeda_br(saldo_atual)
)

col3.metric(
    "🔮 Saldo Previsto",
    moeda_br(saldo_previsto)
)

col4.metric(
    "📊 Variação",
    f"{crescimento:.2f}%"
)

st.divider()

# =====================================
# RECEITA MENSAL
# =====================================

st.subheader("📈 Evolução da Receita Mensal")

df_financeiro["data_transacao"] = pd.to_datetime(
    df_financeiro["data_transacao"]
)

df_financeiro["mes"] = (
    df_financeiro["data_transacao"]
    .dt.strftime("%Y-%m")
)

receita_mensal = (
    df_financeiro
    .groupby("mes")["receita_dia"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10,4))

receita_mensal.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Receita Total por Mês")
ax.set_xlabel("Mês")
ax.set_ylabel("Receita (R$)")
ax.grid(axis="y", linestyle="--", alpha=0.5)

st.pyplot(fig)

# =====================================
# SALDO HISTÓRICO
# =====================================

st.subheader("💰 Histórico do Saldo de Caixa")

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(
    df_financeiro["saldo_caixa"],
    linewidth=2
)

ax.set_title("Evolução do Saldo de Caixa")
ax.set_xlabel("Dias")
ax.set_ylabel("Saldo (R$)")
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# =====================================
# PREVISÃO FUTURA
# =====================================

st.subheader("🔮 Projeção de Caixa para os Próximos 30 Dias")

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(
    df_previsao["saldo_previsto"],
    linewidth=2
)

ax.set_title("Saldo Projetado")
ax.set_xlabel("Dias Futuros")
ax.set_ylabel("Saldo (R$)")
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# =====================================
# IMPORTÂNCIA DAS VARIÁVEIS
# =====================================

st.subheader("🧠 Fatores que Mais Influenciam o Caixa")

fig, ax = plt.subplots(figsize=(10,4))

ax.barh(
    df_importancia["variavel"],
    df_importancia["importancia"]
)

ax.set_title("Importância das Variáveis do Modelo")
ax.set_xlabel("Importância")
ax.grid(axis="x", linestyle="--", alpha=0.5)

st.pyplot(fig)

# =====================================
# INSIGHTS DO MODELO
# =====================================

st.subheader("🔍 Insights do Modelo")

st.markdown(
    """
    Principais fatores que impactam o saldo de caixa:

    - Receita média dos últimos 30 dias

    - Fluxo médio dos últimos 30 dias

    - Receita média dos últimos 7 dias

    O modelo identificou que tendências de médio prazo possuem maior influência no saldo futuro da cafeteria.
    """
)

# =====================================
# ALERTA FINANCEIRO
# =====================================

st.subheader("🚨 Situação Financeira")

if crescimento >= 10:
    st.success("Caixa saudável")

elif crescimento >= -5:
    st.warning("Caixa estável")

else:
    st.error("Atenção: tendência de queda")

# =====================================
# RESUMO EXECUTIVO
# =====================================

st.subheader("📋 Resumo Executivo")

if crescimento >= 10:
    mensagem = (
        f"O Fluxo Inteligente prevê crescimento do saldo de caixa "
        f"de {crescimento:.2f}% nos próximos 30 dias."
    )

elif crescimento >= -5:
    mensagem = (
        f"O Fluxo Inteligente prevê estabilidade financeira "
        f"para os próximos 30 dias, com variação de "
        f"{crescimento:.2f}%."
    )

else:
    mensagem = (
        f"O Fluxo Inteligente identificou uma tendência "
        f"de redução do saldo de caixa de "
        f"{abs(crescimento):.2f}%."
    )

st.info(mensagem)

# =====================================
# RECOMENDAÇÕES GERENCIAIS
# =====================================

st.subheader("🎯 Recomendações Gerenciais")

if crescimento >= 10:

    st.success(
        """
        • O fluxo de caixa apresenta tendência positiva.

        • Considere reinvestir parte do excedente em marketing ou expansão.

        • Não há necessidade imediata de capital de giro adicional.
        """
    )

elif crescimento >= -5:

    st.info(
        """
        • O fluxo de caixa apresenta estabilidade.

        • Recomenda-se acompanhar as vendas semanalmente.

        • Mantenha o controle dos custos operacionais.
        """
    )

else:

    st.error(
        """
        • O modelo identificou tendência de queda no caixa.

        • Avalie ações para aumentar receitas.

        • Considere reforçar o capital de giro.

        • Revise custos fixos e despesas operacionais.
        """
    )
