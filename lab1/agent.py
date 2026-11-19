import re

import anthropic
from config import CONFIG
from dotenv import load_dotenv
from guard import guarded_tool, new_state
from tools import TOOLS
    
load_dotenv()

client = anthropic.Anthropic()
MODEL = CONFIG["model"]
MAX_ITERATIONS = CONFIG["max_iterations"]  # solo red de seguridad

SYSTEM = (
    "Eres un agente de soporte. Consulta el pedido con get_order antes de "
    "cualquier reembolso. Si el cliente pide un humano, escala con "
    "customer_request. Si un reembolso es rechazado por límite o aprobación "
    "humana, escala con policy_gap y explica al cliente que un agente lo "
    "revisará."
)


def run_agent(user_message):
    messages = [{"role": "user", "content": user_message}]
    state = new_state()  # estado del caso, vive en tu código
    has_order_id = re.search(r"\b[A-Z]\d{3}\b", user_message) is not None

    for i in range(MAX_ITERATIONS):
        if i == 0 and has_order_id:
            tool_choice = {"type": "tool", "name": "get_order"}
        else:
            tool_choice = {"type": "auto"}

        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM,
            tools=TOOLS,
            tool_choice=tool_choice,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            results = []
            for block in response.content:
                if block.type == "tool_use":
                    output = guarded_tool(block.name, block.input, state)
                    print(f"[tool] {block.name}({block.input}) -> {output}")
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(output),
                        "is_error": not output["ok"],
                    })
            messages.append({"role": "user", "content": results})
            continue

        raise RuntimeError(f"stop_reason inesperado: {response.stop_reason}")

    raise RuntimeError("Tope de iteraciones alcanzado")


if __name__ == "__main__":
    scenarios = [
        "Quiero el reembolso completo de mi pedido A100.",
        "Quiero el reembolso completo de mi pedido B200.",
        "Quiero un reembolso del pedido Z999.",
        "Quiero hablar con una persona, por favor.",
    ]
    for msg in scenarios:
        print("USER:", msg)
        print("AGENT:", run_agent(msg))
        print("-" * 40)