ORDERS = {
    "A100": {"total": 40.0, "status": "delivered"},
    "B200": {"total": 250.0, "status": "delivered"},
}

TOOLS = [
    {
        "name": "get_order",
        "description": "Consulta un pedido por ID y devuelve su total y estado. "
                       "Debe llamarse antes de cualquier reembolso.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string",
                             "description": "ID del pedido, p. ej. 'A100'."}
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "process_refund",
        "description": "Solicita el reembolso de un monto de un pedido. "
                       "El sistema puede rechazarlo por reglas de negocio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "ID del pedido."},
                "amount": {"type": "number",
                           "description": "Monto a reembolsar en USD."},
            },
            "required": ["order_id", "amount"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Pasa el caso a un agente humano.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string",
                           "enum": ["customer_request", "policy_gap", "no_progress"],
                           "description": "Motivo del escalamiento."}
            },
            "required": ["reason"],
        },
    },
]


def err(category, message):
    return {"ok": False, "error": {"category": category, "message": message}}


def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return err("validation", f"Pedido {order_id} no existe")
    return {"ok": True, "order_id": order_id, **order}


def process_refund(order_id, amount):
    return {"ok": True, "refunded": amount, "order_id": order_id}


def escalate_to_human(reason):
    return {"ok": True, "escalated": True, "reason": reason}


def run_tool(name, args):
    return {"get_order": get_order,
            "process_refund": process_refund,
            "escalate_to_human": escalate_to_human}[name](**args)