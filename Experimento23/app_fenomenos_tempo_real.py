import time
import random
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fenômenos de Tempo Real", layout="wide")

st.title("📈 Simulador de Fenômenos de Tempo Real")
st.write(
    "Este simulador mostra, de forma didática, como a ocupação da CPU, jitter e deadline misses "
    "podem se comportar ao longo do tempo."
)

st.sidebar.header("Parâmetros")
period_ms = st.sidebar.slider("Período da tarefa (ms)", 10, 200, 50)
deadline_ms = st.sidebar.slider("Deadline (ms)", 5, 200, 40)
load_level = st.sidebar.slider("Carga média simulada da CPU (%)", 10, 95, 60)
samples = st.sidebar.slider("Amostras", 50, 400, 150)

st.write(
    f"**Configuração atual:** período = {period_ms} ms, deadline = {deadline_ms} ms, "
    f"carga média = {load_level}%"
)

rows = []
misses = 0

for i in range(samples):
    cpu_occ = max(0, min(100, random.gauss(load_level, 12)))
    exec_time = max(1, random.gauss(period_ms * (cpu_occ / 100.0), period_ms * 0.1))
    jitter = random.gauss(0, period_ms * 0.08)
    response_time = exec_time + abs(jitter)

    miss = response_time > deadline_ms
    if miss:
        misses += 1

    rows.append({
        "amostra": i,
        "cpu_ocupacao_pct": cpu_occ,
        "tempo_exec_ms": exec_time,
        "jitter_ms": jitter,
        "tempo_resposta_ms": response_time,
        "deadline_miss": int(miss),
    })

df = pd.DataFrame(rows)

c1, c2, c3 = st.columns(3)
c1.metric("Misses", misses)
c2.metric("CPU média (%)", f"{df['cpu_ocupacao_pct'].mean():.1f}")
c3.metric("Resposta média (ms)", f"{df['tempo_resposta_ms'].mean():.1f}")

st.subheader("Dados simulados")
st.dataframe(df, use_container_width=True, height=250)

fig1, ax1 = plt.subplots(figsize=(10, 3))
ax1.plot(df["amostra"], df["cpu_ocupacao_pct"])
ax1.set_title("Ocupação da CPU ao longo do tempo")
ax1.set_xlabel("Amostra")
ax1.set_ylabel("CPU (%)")
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 3))
ax2.plot(df["amostra"], df["jitter_ms"])
ax2.axhline(0, linestyle="--")
ax2.set_title("Jitter ao longo do tempo")
ax2.set_xlabel("Amostra")
ax2.set_ylabel("Jitter (ms)")
st.pyplot(fig2)

fig3, ax3 = plt.subplots(figsize=(10, 3))
ax3.plot(df["amostra"], df["tempo_resposta_ms"], label="Tempo de resposta")
ax3.axhline(deadline_ms, linestyle="--", label="Deadline")
ax3.set_title("Tempo de resposta x deadline")
ax3.set_xlabel("Amostra")
ax3.set_ylabel("Tempo (ms)")
ax3.legend()
st.pyplot(fig3)

st.subheader("Execução em tempo quase real")
placeholder = st.empty()
run = st.button("Animar fenômeno")

if run:
    fig_rt, ax_rt = plt.subplots(figsize=(10, 3))
    cpu_vals = []
    xs = []
    for i in range(min(samples, 80)):
        cpu_vals.append(df.loc[i, "cpu_ocupacao_pct"])
        xs.append(i)
        ax_rt.clear()
        ax_rt.plot(xs, cpu_vals)
        ax_rt.set_ylim(0, 100)
        ax_rt.set_title("CPU em tempo quase real")
        ax_rt.set_xlabel("Amostra")
        ax_rt.set_ylabel("CPU (%)")
        placeholder.pyplot(fig_rt)
        time.sleep(0.05)

st.info(
    "Conceitos didáticos: ocupação da CPU, jitter, tempo de resposta, deadline miss e variabilidade temporal."
)
