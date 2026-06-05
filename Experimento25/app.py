
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gantt Interativo", layout="wide")

st.title("📊 Simulador Gantt Interativo — Programação em Tempo Real")
st.write(
    "Este app permite configurar tarefas periódicas e visualizar um diagrama de Gantt didático. "
    "Ele foi pensado para apoiar aulas de Programação em Tempo Real."
)

st.sidebar.header("Configuração geral")
horizonte = st.sidebar.slider("Horizonte de simulação (ticks)", 10, 100, 30)
politica = st.sidebar.selectbox("Política de escalonamento", ["RM", "EDF"])

st.sidebar.header("Tarefas")
n_tasks = st.sidebar.slider("Quantidade de tarefas", 2, 5, 3)

tasks = []
default_vals = [
    ("T1", 1, 4, 4),
    ("T2", 2, 6, 6),
    ("T3", 1, 8, 8),
    ("T4", 2, 10, 10),
    ("T5", 1, 12, 12),
]

for i in range(n_tasks):
    with st.sidebar.expander(f"Tarefa {i+1}", expanded=(i < 3)):
        name = st.text_input(f"Nome {i+1}", value=default_vals[i][0], key=f"name_{i}")
        c = st.number_input(f"C{i+1} (tempo de computação)", min_value=1, max_value=20, value=default_vals[i][1], key=f"c_{i}")
        t = st.number_input(f"T{i+1} (período)", min_value=1, max_value=50, value=default_vals[i][2], key=f"t_{i}")
        d = st.number_input(f"D{i+1} (deadline)", min_value=1, max_value=50, value=default_vals[i][3], key=f"d_{i}")
        tasks.append({"name": name, "C": int(c), "T": int(t), "D": int(d)})

def simulate(tasks, horizon, policy="RM"):
    remaining = {t["name"]: 0 for t in tasks}
    next_release = {t["name"]: 0 for t in tasks}
    abs_deadline = {t["name"]: None for t in tasks}
    releases = []
    misses = []
    gantt = []

    rm_order = sorted(tasks, key=lambda x: x["T"])

    for tick in range(horizon):
        # releases
        for task in tasks:
            if tick == next_release[task["name"]]:
                remaining[task["name"]] += task["C"]
                abs_deadline[task["name"]] = tick + task["D"]
                releases.append((tick, task["name"]))
                next_release[task["name"]] += task["T"]

        # pick task
        running = None
        if policy == "RM":
            for task in rm_order:
                if remaining[task["name"]] > 0:
                    running = task["name"]
                    break
        else:  # EDF
            best_deadline = None
            for task in tasks:
                if remaining[task["name"]] > 0:
                    d = abs_deadline[task["name"]]
                    if best_deadline is None or d < best_deadline:
                        best_deadline = d
                        running = task["name"]

        gantt.append(running)

        if running is not None:
            remaining[running] -= 1

        # deadline misses
        for task in tasks:
            d = abs_deadline[task["name"]]
            if d is not None and tick == d and remaining[task["name"]] > 0:
                misses.append((tick, task["name"]))

    return gantt, releases, misses

gantt, releases, misses = simulate(tasks, horizonte, politica)

st.subheader("Tabela das tarefas")
df_tasks = pd.DataFrame(tasks)
df_tasks["Utilização"] = df_tasks["C"] / df_tasks["T"]
st.dataframe(df_tasks, use_container_width=True)

st.metric("Utilização total da CPU", f"{df_tasks['Utilização'].sum():.2f}")
st.metric("Deadline misses", len(misses))

st.subheader("Diagrama de Gantt")

task_names = [t["name"] for t in tasks]
y_map = {name: idx for idx, name in enumerate(task_names)}
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
color_map = {task["name"]: colors[i % len(colors)] for i, task in enumerate(tasks)}

fig, ax = plt.subplots(figsize=(12, 4 + 0.4 * len(tasks)))

current = None
start = 0
for i, task_name in enumerate(gantt + [None]):
    if task_name != current:
        if current is not None:
            y = y_map[current]
            ax.broken_barh([(start, i - start)], (y - 0.35, 0.7), facecolors=color_map[current], edgecolors="black")
        current = task_name
        start = i

for tick, name in releases:
    y = y_map[name]
    ax.plot(tick, y, marker="o", linestyle="None", color="black")
    ax.text(tick, y + 0.4, "R", fontsize=8, ha="center")

for tick, name in misses:
    y = y_map[name]
    ax.plot(tick, y, marker="x", linestyle="None", color="red", markersize=10)
    ax.text(tick, y - 0.5, "MISS", fontsize=8, ha="center", color="red")

ax.set_yticks(list(y_map.values()))
ax.set_yticklabels(task_names)
ax.set_xlabel("Tempo (ticks)")
ax.set_title(f"Gantt — Política {politica}")
ax.grid(True, axis="x", linestyle="--", alpha=0.4)

st.pyplot(fig)

st.subheader("Timeline detalhada")
timeline_df = pd.DataFrame({
    "tick": list(range(horizonte)),
    "executando": gantt
})
st.dataframe(timeline_df, use_container_width=True, height=250)

st.subheader("Como interpretar")
# st.markdown(
#     "- **R** indica liberação de tarefa  
# "
#     "- **MISS** indica deadline perdido  
# "
#     "- blocos coloridos mostram quando a CPU executou cada tarefa  
# "
#     "- altere C, T e D para observar mudanças no comportamento"
# )

st.info(
    "Sugestão didática: compare RM e EDF com os mesmos parâmetros. "
    "Depois aumente C de uma tarefa até surgirem deadline misses."
)
