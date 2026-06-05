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
import threading
import queue
import random

# ============================================================
# CONCEITO: Comunicação entre tarefas via fila (queue)
# ============================================================
# Filas são mecanismos clássicos em RTOS:
#   - produtor gera dados (sensor)
#   - consumidor processa (controle, log, transmissão)
#
# Fila com maxsize modela buffer finito:
#   - se enche, produtor bloqueia
#   - isso afeta latência (idade do item)

q = queue.Queue(maxsize=5)

def producer():
    for i in range(30):
        item = (i, time.perf_counter())
        q.put(item)
        print(f"[P] produz {i}")
        time.sleep(random.uniform(0.08, 0.15))

def consumer():
    for _ in range(30):
        i, ts = q.get()
        age_ms = (time.perf_counter() - ts) * 1000
        print(f"    [C] consome {i}  idade={age_ms:.1f}ms")
        time.sleep(random.uniform(0.02, 0.09))
        q.task_done()

tp = threading.Thread(target=producer)
tc = threading.Thread(target=consumer)
tp.start(); tc.start()
tp.join(); tc.join()

print("\nDiscussão sugerida:")
print("- O que acontece com a 'idade' quando o consumidor é mais lento?")
print("- Fila grande pode aumentar latência e piorar deadlines.")
