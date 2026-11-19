# Fuentes simuladas (datos inventados para el lab)
SOURCES = [
    {
        "id": "S1",
        "topic": "solar",
        "text": "País A: la capacidad solar instalada creció 30% en 2025.",
    },
    {
        "id": "S2",
        "topic": "solar",
        "text": "País B: el costo por MWh solar bajó a 28 USD en 2025.",
    },
    {
        "id": "S3",
        "topic": "wind",
        "text": "País A: la eólica marina aportó 12% de la electricidad en 2025.",
    },
    {
        "id": "S4",
        "topic": "storage",
        "text": "País C: el almacenamiento en baterías se duplicó entre 2024 y 2025.",
    },
    {
        "id": "S5",
        "topic": "nuclear",
        "text": "Francia trabaja en aumentar su produccion de energia nuclear para 2030"
    }
]


def search_sources(topic):
    results = [s for s in SOURCES if s["topic"] == topic.lower().strip()]
    # "sin resultados" NO es un fallo: ok=True y results vacío
    return {"ok": True, "topic": topic, "results": results}
