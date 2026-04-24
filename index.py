import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Corrida", layout="wide")

df = pd.read_csv("activities.csv")

df["Data"] = pd.to_datetime(df["Data"])
df["Semana"] = df["Data"].dt.isocalendar().week

st.title("Dashboard de Treinos de Corrida")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Treinos", len(df))
col2.metric("KM Totais", round(df["Distância"].sum(),1))
col3.metric("Horas Totais", round(df["Tempo"].sum()/3600,1))
col4.metric("Pace Médio", round(df["Ritmo"].mean(),2))

st.divider()

# KM por semana
weekly = df.groupby("Semana")["Distância"].sum().reset_index()

fig = px.bar(
    weekly,
    x="Semana",
    y="Distância",
    title="Volume semanal (km)"
)

st.plotly_chart(fig, use_container_width=True)

# evolução pace
fig2 = px.line(
    df,
    x="Data",
    y="Ritmo",
    title="Evolução do Pace"
)

st.plotly_chart(fig2, use_container_width=True)

# FC vs Pace
fig3 = px.scatter(
    df,
    x="FC Média",
    y="Ritmo",
    title="Pace vs Frequência Cardíaca"
)

st.plotly_chart(fig3, use_container_width=True)

# distribuição distâncias
fig4 = px.histogram(
    df,
    x="Distância",
    title="Distribuição das distâncias"
)

st.plotly_chart(fig4, use_container_width=True)