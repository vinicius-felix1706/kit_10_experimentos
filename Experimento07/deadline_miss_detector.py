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
import random

# ============================================================
# CONCEITO: Deadline (prazo) e detecção de perda de prazo
# ============================================================
# Formalização simples de tempo real:
#   Para cada tarefa i:
#       Tempo de resposta Ri <= Deadline Di
#   Se Ri > Di, o sistema falhou (mesmo com resposta correta).
#
# Aqui simulamos uma tarefa periódica com tempo de execução variável.
# Algumas instâncias ultrapassarão o deadline -> "deadline miss".

PERIOD = 0.05     # 50 ms
DEADLINE = 0.04   # 40 ms
N = 50

next_release = time.perf_counter()
misses = 0

for i in range(N):
    # Espera o instante de liberação (release)
    now = time.perf_counter()
    if now < next_release:
        time.sleep(next_release - now)

    start = time.perf_counter()

    # "Workload" variável (simula computação variando)
    work = random.uniform(0.010, 0.060)  # 10–60 ms
    time.sleep(work)

    finish = time.perf_counter()
    R = finish - start

    ok = R <= DEADLINE
    if not ok:
        misses += 1

    print(f"T{i:02d} exec={R*1000:.1f}ms  deadline={DEADLINE*1000:.1f}ms  {'OK' if ok else 'MISS'}")
    next_release += PERIOD

print(f"\nTotal deadline misses: {misses}/{N}")

print("\nDiscussão sugerida:")
print("- Por que um sistema pode falhar mesmo calculando corretamente?")
print("- Como reduzir misses? (otimização, priorização, RTOS, redução de carga)")
