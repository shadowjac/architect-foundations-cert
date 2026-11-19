import json

from coordinator import plan

questions = [
    "Compara solar, eólica, nuclear y almacenamiento en baterías en 2025.",
    "Resume qué pasó con la energía solar y la energia nuclear en 2025.",
    "Averigua en que trabaja homero simpson"
]

for q in questions:
    print("PREGUNTA:", q)
    print(json.dumps(plan(q), indent=2, ensure_ascii=False))
    print("-" * 40)