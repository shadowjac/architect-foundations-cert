from tools import err, run_tool

REFUND_LIMIT = 100.0

def new_state():
    return{"verified_orders": {}}

def guarded_tool(name, args, state):
    if name == "get_order":
        result = run_tool(name, args)
        if result["ok"]:
            state["verified_orders"][args["order_id"]] = result["total"]
        return result

    if name == "process_refund":
        order_id, amount = args["order_id"], args["amount"]

        if order_id not in state["verified_orders"]:
            return err("business", "Consulta el pedido con get_order antes de solicitar un reembolso")
        total = state["verified_orders"][order_id]
        if amount <= 0 or amount > total:
            return err("validation", f"Monto inválido: debe ser > 0 y <= {total}")

        if amount > REFUND_LIMIT:
            return err("business", f"El monto máximo de reembolso es {REFUND_LIMIT} USD "
                                    "Requiere aprobación de un humano para montos mayores.")

    return run_tool(name, args)