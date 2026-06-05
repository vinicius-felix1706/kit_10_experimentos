"""
Example 3 — CPU Overload

Concepts illustrated
- CPU contention
- Interference between tasks
- Timing disruption

Goal
Show how a heavy computation can disturb periodic behavior.
"""

import time

period = 0.02

while True:

    start = time.time()

    # Heavy computation
    x = 0
    for i in range(10000000):
        x += i

    elapsed = time.time() - start

    print("Execution time:", elapsed)

    sleep_time = period - elapsed

    if sleep_time > 0:
        time.sleep(sleep_time)
