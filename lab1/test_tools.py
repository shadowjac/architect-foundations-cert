from tools import run_tool

print(run_tool("get_order", {"order_id": "A100"}))
print(run_tool("get_order", {"order_id": "ZZZ"}))