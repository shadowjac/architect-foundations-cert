import anthropic
from dotenv import load_dotenv

from config import CONFIG

load_dotenv()
client = anthropic.Anthropic()
MODEL = CONFIG["model"]

SYNTH_SYSTEM = (
    "Redactas la respuesta final de un informe a partir de hallazgos de "
    "investigación. Usa solo los hallazgos entregados; no añadas datos ni "
    "conocimiento propio. Cita los IDs de fuente entre corchetes. "
    "Máximo 120 palabras, en español."
)


def synthesize(question, answered):
    if not answered:
        return "No hay hallazgos para sintetizar."

    findings = "\n\n".join(
        f"[{r['task_id']}] fuentes {r['source_ids']}: {r['summary']}"
        for r in answered
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=SYNTH_SYSTEM,
        messages=[{"role": "user",
                   "content": f"PREGUNTA: {question}\n\nHALLAZGOS:\n{findings}"}],
    )
    if response.stop_reason != "end_turn":
        raise RuntimeError(f"stop_reason inesperado: {response.stop_reason}")
    return "".join(b.text for b in response.content if b.type == "text")


def coverage(subtasks, parts):
    # lo arma el código, no el modelo
    objective = {t["id"]: t["objective"] for t in subtasks}
    lines = []
    for r in parts["answered"]:
        lines.append(f"- Respondida: {objective[r['task_id']]} "
                     f"(fuentes {r['source_ids']})")
    for r in parts["no_sources"]:
        lines.append(f"- Sin fuentes: {objective[r['task_id']]}")
    for r in parts["failed"]:
        lines.append(f"- Falló: {objective[r['task_id']]} "
                     f"({r['error']['category']})")
    return "\n".join(lines)