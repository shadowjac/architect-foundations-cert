import anthropic
from data import search_sources
from dotenv import load_dotenv

from config import CONFIG

load_dotenv()

client = anthropic.Anthropic()

SUBAGENT_SYSTEM = (
    "Eres un subagente de investigación. Usa solo la herramienta "
    "search_sources. Responde únicamente con lo que devuelvan las fuentes, "
    "citando sus IDs. Si no hay resultados, dilo explícitamente; no inventes."
)

SUBAGENT_TOOLS = [
    {
        "name": "search_sources",
        "description": "Busca fuentes locales por tema. Recibe una sola palabra "
        "en inglés. Temas con fuentes: 'solar', 'wind', 'storage'. "
        "Cualquier otro tema devuelve vacío.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Tema a buscar, una palabra.",
                }
            },
            "required": ["topic"],
        },
    }
]


def build_prompt(task):
    # el subagente no ve la conversación: todo va aquí
    return (
        f"OBJETIVO: {task['objective']}\n"
        f"CONTEXTO: {task['context']}\n"
        f"HERRAMIENTAS PERMITIDAS: search_sources\n"
        f"FORMATO DE SALIDA: {task['output_format']}"
    )


def run_subagent(task):
    messages = [{"role": "user", "content": build_prompt(task)}]
    used_ids = set()  # para evitar repetir fuentes

    for _ in range(CONFIG["max_iterations"]):
        response = client.messages.create(
            model=CONFIG["model"],
            max_tokens=1000,
            system=SUBAGENT_SYSTEM,
            tools=SUBAGENT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            text = "".join(b.text for b in response.content if b.type == "text")
            return {
                "ok": True,
                "task_id": task["id"],
                "summary": text,
                "source_ids": sorted(used_ids),
            }

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = []

            for block in response.content:
                if block.type == "tool_use":
                    output = search_sources(**block.input)
                    used_ids.update(r["id"] for r in output["results"])
                    results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(output),
                        }
                    )
            messages.append({"role": "user", "content": results})
            continue

        raise RuntimeError(f"stop_reason inesperado: {response.stop_reason}")

    raise RuntimeError("Tope de iteraciones alcanzado")
