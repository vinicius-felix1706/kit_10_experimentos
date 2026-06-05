import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Semáforo", layout="wide")

st.title("🚦 Simulador de Semáforo em Tempo Real")
st.write(
    "Este simulador mostra um cruzamento simples com dois fluxos: Norte-Sul e Leste-Oeste. "
    "A lógica alterna os sinais e permite observar ciclos temporais, tempos de verde, amarelo e vermelho."
)

col1, col2 = st.columns(2)
with col1:
    green_ns = st.slider("Tempo verde Norte-Sul (s)", 5, 30, 10)
    yellow_ns = st.slider("Tempo amarelo Norte-Sul (s)", 2, 10, 3)
with col2:
    green_ew = st.slider("Tempo verde Leste-Oeste (s)", 5, 30, 10)
    yellow_ew = st.slider("Tempo amarelo Leste-Oeste (s)", 2, 10, 3)

cycles = st.slider("Quantidade de ciclos para simulação", 1, 10, 3)

phases = [
    ("Norte-Sul VERDE", green_ns),
    ("Norte-Sul AMARELO", yellow_ns),
    ("Leste-Oeste VERDE", green_ew),
    ("Leste-Oeste AMARELO", yellow_ew),
]

timeline = []
t = 0
for _ in range(cycles):
    for phase, duration in phases:
        for _ in range(duration):
            timeline.append({"tempo_s": t, "fase": phase})
            t += 1

df = pd.DataFrame(timeline)

st.subheader("Linha do tempo do semáforo")
st.dataframe(df, use_container_width=True, height=300)

phase_colors = {
    "Norte-Sul VERDE": "green",
    "Norte-Sul AMARELO": "gold",
    "Leste-Oeste VERDE": "blue",
    "Leste-Oeste AMARELO": "orange",
}

fig, ax = plt.subplots(figsize=(12, 3))
for _, row in df.iterrows():
    ax.barh(0, 1, left=row["tempo_s"], color=phase_colors[row["fase"]], edgecolor="black")
ax.set_yticks([])
ax.set_xlabel("Tempo (s)")
ax.set_title("Diagrama temporal do semáforo")
st.pyplot(fig)

st.subheader("Animação textual")
placeholder = st.empty()
run = st.button("Executar animação")

if run:
    for _, row in df.iterrows():
       placeholder.markdown(
        f"### Tempo: {row['tempo_s']} s\n\n"
        f"**Fase atual:** `{row['fase']}`"
)
time.sleep(0.2)

st.info(
    "Conceitos didáticos: tarefas periódicas, ciclos de controle, temporização e sincronização."
)
