
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Laboratório de Jitter", layout="wide")

st.title("📈 Laboratório de Jitter, Latência e CPU")
st.write(
    "Simule o comportamento temporal de uma tarefa periódica sob diferentes níveis de carga. "
    "O objetivo é observar **jitter**, **tempo de resposta**, **ocupação de CPU** e **deadline misses**."
)

with st.sidebar:
    st.header("Parâmetros")
    period_ms = st.slider("Período da tarefa (ms)", 5, 200, 50)
    deadline_ms = st.slider("Deadline (ms)", 5, 250, 40)
    cpu_load = st.slider("Carga média simulada da CPU (%)", 5, 95, 60)
    noise = st.slider("Ruído temporal (%)", 1, 40, 10)
    n = st.slider("Amostras", 50, 400, 150)

rows = []
misses = 0
for i in range(n):
    cpu_occ = max(0, min(100, random.gauss(cpu_load, 8)))
    exec_ms = max(1, random.gauss(period_ms * (cpu_occ / 100), period_ms * (noise / 100)))
    jitter_ms = random.gauss(0, period_ms * (noise / 100) * 0.5)
    response_ms = exec_ms + abs(jitter_ms)
    miss = response_ms > deadline_ms
    misses += int(miss)

    rows.append({
        "amostra": i,
        "cpu_%": cpu_occ,
        "exec_ms": exec_ms,
        "jitter_ms": jitter_ms,
        "response_ms": response_ms,
        "miss": int(miss),
    })

df = pd.DataFrame(rows)

c1, c2, c3 = st.columns(3)
c1.metric("Misses", misses)
c2.metric("CPU média", f"{df['cpu_%'].mean():.1f}%")
c3.metric("Resposta média", f"{df['response_ms'].mean():.1f} ms")

st.dataframe(df, use_container_width=True, height=250)

fig1, ax1 = plt.subplots(figsize=(10, 3))
ax1.plot(df["amostra"], df["cpu_%"])
ax1.set_title("Ocupação da CPU")
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
ax3.plot(df["amostra"], df["response_ms"], label="Tempo de resposta")
ax3.axhline(deadline_ms, linestyle="--", label="Deadline")
ax3.set_title("Tempo de resposta x deadline")
ax3.set_xlabel("Amostra")
ax3.set_ylabel("Tempo (ms)")
ax3.legend()
st.pyplot(fig3)

st.subheader("Modo exercício")
st.markdown(
    "Use o simulador para responder:\n"
    "1. O que acontece com os misses quando a carga média da CPU aumenta?\n"
    "2. Como o ruído temporal afeta o jitter?\n"
    "3. É possível ter CPU média moderada e ainda assim perder deadlines?\n"
    "4. O que muda ao aumentar o período mantendo o mesmo nível de carga?"
)

with st.expander("Pistas de interpretação"):
    st.markdown(
        "- **Jitter** = variação temporal em torno do comportamento esperado.\n"
        "- **Tempo de resposta** maior que o deadline implica **deadline miss**.\n"
        "- Mesmo com CPU média abaixo de 100%, o sistema pode perder deadlines.\n"
        "- Ruído maior tende a espalhar mais a distribuição temporal."
    )
