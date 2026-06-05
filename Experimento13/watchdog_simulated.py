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
# CONCEITO: Watchdog Timer (WDT) — simulação
# ============================================================
# Watchdog reinicia o sistema se o software parar de responder.
# A tarefa principal deve "alimentar" (kick) periodicamente.

last_kick = time.perf_counter()
LOCK = threading.Lock()

def watchdog(timeout_s=0.3):
    global last_kick
    while True:
        time.sleep(0.05)
        with LOCK:
            age = time.perf_counter() - last_kick
        if age > timeout_s:
            print(f"[WDT] TIMEOUT! sem kick há {age*1000:.1f}ms -> reset (simulado)")
            break

def main_task():
    global last_kick
    for _ in range(30):
        if random.random() < 0.08:
            print("[MAIN] travou (simulado)...")
            time.sleep(0.6)
        with LOCK:
            last_kick = time.perf_counter()
        print("[MAIN] kick")
        time.sleep(0.05)

threading.Thread(target=watchdog, daemon=True).start()
main_task()
