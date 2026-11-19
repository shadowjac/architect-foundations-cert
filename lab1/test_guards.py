from guard import guarded_tool, new_state


def show(label, result):
    print(label, "->", result)


s = new_state()
show("1 reembolso sin get_order",
     guarded_tool("process_refund", {"order_id": "A100", "amount": 40.0}, s))

s = new_state()
guarded_tool("get_order", {"order_id": "A100"}, s)
show("2 reembolso A100 40",
     guarded_tool("process_refund", {"order_id": "A100", "amount": 40.0}, s))
show("3 monto negativo",
     guarded_tool("process_refund", {"order_id": "A100", "amount": -5.0}, s))

s = new_state()
guarded_tool("get_order", {"order_id": "B200"}, s)
show("4 B200 $250 (sobre el límite)",
     guarded_tool("process_refund", {"order_id": "B200", "amount": 250.0}, s))
show("5 B200 $300 (mayor que el total)",
     guarded_tool("process_refund", {"order_id": "B200", "amount": 300.0}, s))