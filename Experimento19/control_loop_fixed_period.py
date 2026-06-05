"""Programação em Tempo Real (conceitos) — Demonstrações em Python

IMPORTANTE (para explicar em sala):
- Python em um PC com Windows/Linux/macOS NÃO garante "hard real-time".
- Estes exemplos servem para visualizar conceitos: periodicidade, deadline, latência, jitter,
  concorrência, comunicação, bloqueios e escalonamento.
- No mundo real embarcado (ex.: ESP32 + FreeRTOS), usamos RTOS para aumentar previsibilidade.

Como executar:
  python nome_do_arquivo.py
"""

import time
import math
import random

# ============================================================
# CONCEITO: Loop de controle periódico + overrun
# ============================================================
# Uma malha de controle:
# 1) lê sensor
# 2) calcula controle
# 3) atua
# deve repetir com período fixo. Overrun ocorre se a execução excede o período.

PERIOD = 0.02
N = 200

x = 0.0
u = 0.0

next_t = time.perf_counter() + PERIOD
overruns = 0

for k in range(N):
    now = time.perf_counter()
    if now < next_t:
        time.sleep(next_t - now)

    ref = math.sin(2 * math.pi * 0.5 * (k * PERIOD))
    meas = x + random.uniform(-0.02, 0.02)

    Kp = 1.2
    u = Kp * (ref - meas)

    x = 0.9 * x + 0.1 * u

    # carga variável: até 10ms
    time.sleep(random.uniform(0.0, 0.010))

    finish = time.perf_counter()
    if finish > next_t:
        overruns += 1

    print(f"k={k:03d} ref={ref:+.2f} x={x:+.2f} u={u:+.2f}  overruns={overruns}")
    next_t += PERIOD

print("\nOverruns:", overruns)
