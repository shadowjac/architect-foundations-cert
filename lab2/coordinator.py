import anthropic
from dotenv import load_dotenv

from config import CONFIG

load_dotenv()

client = anthropic.Anthropic()

MODEL = CONFIG["model"]
MAX_SUBTASKS = 5

PLANNER_SYSTEM = (
    "Eres el coordinador de un equipo de investigación. Divide la pregunta "
    "en subtareas independientes entre sí, una por tema. Cada subagente "
    "busca en fuentes locales por palabra clave y NO ve esta conversación: "
    "el contexto de cada subtarea debe bastarse por sí solo. Si la pregunta "
    "trata un solo tema, crea una sola subtarea."
)

PLAN_TOOL = {
    "name": "create_plan",
    "description": "Divide la pregunta en subtareas de investigación "
    "independientes entre sí.",
    "input_schema": {
        "type": "object",
        "properties": {
            "in_scope": {
                "type": "boolean",
                "description": "true solo si la pregunta trata de energía "
                "(solar, eólica, almacenamiento, nuclear...).",
            },
            "subtasks": {
                "type": "array",
                "description": "Entre 1 y 5 subtareas si in_scope es true; "
                "lista vacía si es false.",
                "items": {
                    "type": "object",
                    "properties": {
                        "objective": {
                            "type": "string",
                            "description": "Qué debe investigar el subagente, "
                            "en una frase.",
                        },
                        "context": {
                            "type": "string",
                            "description": "Contexto de la pregunta original "
                            "que el subagente necesita.",
                        },
                        "output_format": {
                            "type": "string",
                            "description": "Formato esperado del resultado.",
                        },
                    },
                    "required": ["objective", "context", "output_format"],
                },
            },
        },
        "required": ["in_scope", "subtasks"],
    },
}


def validate_plan(in_scope, raw):
    if not isinstance(in_scope, bool) or not isinstance(raw, list):
        raise TypeError("Plan inválido: forma incorrecta")
    if not in_scope:
        if raw:
            raise ValueError("Fuera de alcance no debe traer subtareas")
        return
    if not 1 <= len(raw) <= MAX_SUBTASKS:
        raise ValueError(f"Plan inválido: se esperaban 1-{MAX_SUBTASKS} subtareas")
    for s in raw:
        for key in ("objective", "context", "output_format"):
            if not isinstance(s.get(key), str) or not s[key].strip():
                raise ValueError(f"Subtarea inválida: falta '{key}'")


def plan(question):
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=PLANNER_SYSTEM,
        tools=[PLAN_TOOL],
        tool_choice={"type": "tool", "name": "create_plan"},
        messages=[{"role": "user", "content": question}],
    )
    if response.stop_reason != "tool_use":
        raise RuntimeError(f"stop_reason inesperado: {response.stop_reason}")

    block = next(b for b in response.content if b.type == "tool_use")
    in_scope = block.input.get("in_scope")
    raw = block.input.get("subtasks")
    validate_plan(in_scope, raw)

    if not in_scope:
        return {"in_scope": False, "subtasks": []}

    # los IDs los asigna tu código, no el modelo
    return {"in_scope": True,
            "subtasks": [{"id": f"t{i}", **s} for i, s in enumerate(raw, 1)]}