import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# =====================================
# FORMATAÇÃO BRASILEIRA
# =====================================

def formatar_moeda(valor):
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
# SOBRE O PROJETO
# =====================================

st.markdown(
    """
    ---
    ### ☕ Sobre o Fluxo Inteligente

    O Fluxo Inteligente é um protótipo SaaS de Inteligência Financeira
    desenvolvido para pequenas cafeterias.

    Utilizando técnicas de Ciência de Dados e Machine Learning,
    o sistema projeta o saldo de caixa futuro e gera recomendações
    para apoiar a tomada de decisão financeira.

    **Principais funcionalidades:**
    
    ✅ Monitoramento financeiro
    
    ✅ Projeção de saldo de caixa
    
    ✅ Identificação dos fatores que impactam o caixa
    
    ✅ Recomendações gerenciais automatizadas
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

df_historico_previsao = pd.read_csv(
    "dados/historico_previsao_fluxo_inteligente.csv"
)

df_historico_previsao["data"] = pd.to_datetime(
    df_historico_previsao["data"]
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

st.subheader("📌 Indicadores Financeiros")

st.caption(
    "Resumo dos principais indicadores financeiros gerados pelo Fluxo Inteligente."
)

receita_total = df_financeiro["receita_dia"].sum()

saldo_atual = df_financeiro["saldo_caixa"].iloc[-1]

saldo_previsto = df_previsao["saldo_previsto"].iloc[-1]

crescimento = (
    (saldo_previsto - saldo_atual)
    / saldo_atual
) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💵 Receita Total",
    formatar_moeda(receita_total)
)

col2.metric(
    "💰 Saldo Atual",
    formatar_moeda(saldo_atual)
)

col3.metric(
    "🔮 Saldo Previsto",
    formatar_moeda(saldo_previsto)
)

col4.metric(
    "📈 Variação",
    f"{crescimento:.2f}".replace(".", ",") + "%"
)

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Visão Geral",
        "📈 Análises",
        "🤖 Inteligência"
    ]
)

with tab1:
    # =====================================
    # RECEITA MENSAL + SALDO HISTÓRICO
    # =====================================
    
    col_graf1, col_graf2 = st.columns(2)
    
    # ---------- RECEITA MENSAL ----------
    
    with col_graf1:
    
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
            .groupby("mes", as_index=False)["receita_dia"]
            .sum()
        )
    
        fig = px.bar(
            receita_mensal,
            x="mes",
            y="receita_dia",
            text_auto=".2s",
            title="Receita Total por Mês"
        )
    
        fig.update_layout(
            xaxis_title="Mês",
            yaxis_title="Receita (R$)",
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=50, b=20)
        )
    
        st.plotly_chart(fig, use_container_width=True)
    
    
    # ---------- SALDO HISTÓRICO ----------
    
    with col_graf2:
    
        st.subheader("💰 Evolução do Saldo de Caixa")
    
        saldo = df_financeiro.reset_index()
    
        fig = px.line(
            saldo,
            x=saldo.index,
            y="saldo_caixa",
            title="Saldo de Caixa"
        )
    
        fig.update_traces(
            line=dict(width=3)
        )
    
        fig.update_layout(
            xaxis_title="Dias",
            yaxis_title="Saldo (R$)",
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=50, b=20)
        )
    
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # =====================================
    # PREVISÃO + IMPORTÂNCIA DAS VARIÁVEIS
    # =====================================
    
    col_graf3, col_graf4 = st.columns(2)
    
    # ---------- PREVISÃO ----------
    
    with col_graf3:

        st.subheader("🔮 Histórico e Previsão do Saldo de Caixa")
    
        fig = px.line(
            df_historico_previsao,
            x="data",
            y="saldo",
            color="tipo",
            line_dash="tipo",
            title="Evolução Histórica e Projeção do Saldo de Caixa",
            labels={
                "data": "Data",
                "saldo": "Saldo de Caixa (R$)",
                "tipo": "Período"
            }
        )
    
        # Marca o início da previsão
        ultima_data_historico = (
            df_historico_previsao[
                df_historico_previsao["tipo"] == "Histórico"
            ]["data"].max()
        )
    
        fig.add_vline(
            x=ultima_data_historico,
            line_dash="dot",
            line_color="red",
            annotation_text="Início da previsão",
            annotation_position="top right"
        )
    
        fig.update_layout(
            template="plotly_white",
            height=450,
            legend_title="Período"
        )
    
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    
    # ---------- IMPORTÂNCIA DAS VARIÁVEIS ----------
    
    with col_graf4:
    
        st.subheader("📊 Variáveis Mais Importantes")
    
        importancia = df_importancia.sort_values(
            by="importancia",
            ascending=True
        )
    
        fig = px.bar(
            importancia,
            x="importancia",
            y="variavel",
            orientation="h",
            title="Importância das Variáveis",
            text_auto=".2f"
        )
    
        fig.update_layout(
            xaxis_title="Importância",
            yaxis_title="",
            template="plotly_white",
            height=420,
            margin=dict(l=20, r=20, t=50, b=20)
        )
    
        st.plotly_chart(fig, use_container_width=True)

with tab3:
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

# =====================================
# RODAPÉ
# =====================================

st.divider()

st.caption(
    """
    ☕ **Fluxo Inteligente** • Sistema de Inteligência Financeira para Pequenas Cafeterias

    Desenvolvido por **Estefane Andrade**

    Especialização em Ciência de Dados — UTFPR • 2026
    """
)


