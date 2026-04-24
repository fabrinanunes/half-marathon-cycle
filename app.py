import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Treinos",
    layout="wide"
)

st.title("🏃 Dashboard de Treinos de Corrida")

# -----------------------------
# Carregar dados
# -----------------------------

df = pd.read_csv(
    "activities.csv",
    sep=";",
    decimal=",",
    engine="python"
)

# -----------------------------
# Limpeza e preparação
# -----------------------------

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

df["Distância"] = pd.to_numeric(df["Distância"], errors="coerce")

df["Tempo"] = pd.to_timedelta(df["Tempo"], errors="coerce")

df["Horas"] = df["Tempo"].dt.total_seconds() / 3600

df["Semana"] = df["Data"].dt.isocalendar().week

df["Ano"] = df["Data"].dt.year

df["Ritmo médio"] = pd.to_numeric(df["Ritmo médio"], errors="coerce")

df["FC Média"] = pd.to_numeric(df["FC Média"], errors="coerce")

df["Cadência de corrida média"] = pd.to_numeric(
    df["Cadência de corrida média"],
    errors="coerce"
)

# manter apenas corridas
df = df[df["Tipo de atividade"].str.contains("Run", na=False)]

# -----------------------------
# KPIs
# -----------------------------

total_treinos = len(df)
total_km = df["Distância"].sum()
total_horas = df["Horas"].sum()
semanas = df["Semana"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Treinos", total_treinos)
col2.metric("KM Totais", round(total_km, 1))
col3.metric("Horas Totais", round(total_horas, 1))
col4.metric("Semanas treinadas", semanas)

st.divider()

# -----------------------------
# Volume semanal
# -----------------------------

volume_semanal = (
    df.groupby("Semana")["Distância"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    volume_semanal,
    x="Semana",
    y="Distância",
    title="Volume semanal (km)"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Evolução do pace
# -----------------------------

fig2 = px.line(
    df,
    x="Data",
    y="Ritmo médio",
    title="Evolução do ritmo médio"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Distâncias dos treinos
# -----------------------------

fig3 = px.histogram(
    df,
    x="Distância",
    nbins=20,
    title="Distribuição das distâncias"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Pace vs FC
# -----------------------------

fig4 = px.scatter(
    df,
    x="FC Média",
    y="Ritmo médio",
    size="Distância",
    hover_data=["Data", "Título"],
    title="Ritmo vs Frequência Cardíaca"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Cadência
# -----------------------------

fig5 = px.scatter(
    df,
    x="Cadência de corrida média",
    y="Ritmo médio",
    size="Distância",
    title="Cadência vs Ritmo"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Longões
# -----------------------------

longoes = df[df["Distância"] >= 15]

fig6 = px.bar(
    longoes,
    x="Data",
    y="Distância",
    title="Longões (15km+)"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# Tabela completa
# -----------------------------

st.subheader("Tabela de treinos")

st.dataframe(
    df.sort_values("Data", ascending=False),
    use_container_width=True
)