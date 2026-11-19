from subagent import run_subagent

FORMAT = "2-3 frases en español, citando IDs de fuentes entre corchetes."

tasks = [
    {
        "id": "t1",
        "objective": "Resumir hallazgos sobre energía solar",
        "context": "Informe comparativo 2025 entre países.",
        "output_format": FORMAT,
    },
    {
        "id": "t2",
        "objective": "Resumir hallazgos sobre energía nuclear",
        "context": "Informe comparativo 2025 y a futuro entre países.",
        "output_format": FORMAT,
    },
]

for t in tasks:
    print(t["id"], "->", run_subagent(t))
    print("-" * 40)
