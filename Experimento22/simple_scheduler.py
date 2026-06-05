"""
Example 4 — Simple Task Scheduler

Concepts illustrated
- Multiple periodic tasks
- Task activation
- Basic scheduler logic

Goal
Simulate multiple tasks with different periods.
"""

import time

tasks = [
    ("sensor", 0.02),
    ("motor_control", 0.05),
    ("communication", 0.2)
]

last_run = {name: time.time() for name, _ in tasks}

print("Starting simple scheduler...")

while True:

    now = time.time()

    for name, period in tasks:

        if now - last_run[name] >= period:

            print("Running task:", name)
            last_run[name] = now

    time.sleep(0.001)
