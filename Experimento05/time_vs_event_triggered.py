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
import random

# ============================================================
# CONCEITO: Time-triggered vs Event-triggered
# ============================================================
# Time-triggered:
#   - execução por tempo (ticks periódicos)
#   - alta previsibilidade
#
# Event-triggered:
#   - execução por eventos/interrupções
#   - pode ser mais responsivo, porém mais difícil de analisar

def time_triggered(duration_s=2.0, period_s=0.05):
    print("\n[Time-triggered] loop periódico (tick)")
    t_end = time.perf_counter() + duration_s
    next_t = time.perf_counter()
    while time.perf_counter() < t_end:
        print("tick")
        next_t += period_s
        sleep = next_t - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)

def event_triggered(duration_s=2.0):
    print("\n[Event-triggered] reage a eventos")
    evt = threading.Event()

    def producer():
        t_end = time.perf_counter() + duration_s
        while time.perf_counter() < t_end:
            time.sleep(random.uniform(0.02, 0.25))
            evt.set()

    threading.Thread(target=producer, daemon=True).start()

    t_end = time.perf_counter() + duration_s
    while time.perf_counter() < t_end:
        if evt.wait(timeout=0.3):
            evt.clear()
            print("evento -> responde")

time_triggered()
event_triggered()

print("\nDiscussão sugerida:")
print("- Qual abordagem é mais previsível?")
print("- Qual é mais eficiente quando eventos são raros?")
