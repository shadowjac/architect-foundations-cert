import time

from coordinator import plan
from orchestrator import run_subagents

QUESTION = "Compara nuclear y almacenamiento en baterías en 2025."
# QUESTION = "Compara solar, eólica, nuclear y almacenamiento en baterías en 2025."

subtasks = plan(QUESTION)["subtasks"]
print(len(subtasks), "subtareas")

for parallel in (False, True):
    start = time.perf_counter()
    results = run_subagents(subtasks, parallel=parallel)
    print(f"parallel={parallel}: {time.perf_counter() - start:.1f}s")

print()
for r in results:
    print(r["task_id"], r["source_ids"], "|", r["summary"][:10000])
