import anthropic
from config import CONFIG

client = anthropic.Anthropic()

r = client.messages.create(
    model=CONFIG["model"],
    max_tokens=200,
    messages=[{
        "role": "user",
        "content": "Responde solo ok"
    }]
)

print(r.content[0].text)
print(r.stop_reason)