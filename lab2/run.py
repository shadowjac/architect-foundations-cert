from coordinator import plan
from orchestrator import partition, run_subagents
from synthesis import coverage, synthesize

QUESTIONS = [
    "Compara solar, eólica, hidrógeno verde y almacenamiento en baterías en 2025.",
    "¿En qué trabaja Homero Simpson?",
]

for q in QUESTIONS:
    print("PREGUNTA:", q)
    p = plan(q)
    if not p["in_scope"]:
        print("Fuera de alcance: no se delegó nada.")
    else:
        results = run_subagents(p["subtasks"])
        parts = partition(results)
        print(synthesize(q, parts["answered"]))
        print("\nCOBERTURA")
        print(coverage(p["subtasks"], parts))
    print("-" * 40)