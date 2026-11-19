# Architect Foundations: labs

Labs prácticos en Python con el SDK de Anthropic para preparar la
certificación Claude Certified Architect – Foundations (CCAR-F).

## Labs

| Lab | Tema | Dominios que practica |
|---|---|---|
| [lab1](lab1/) | Agente de soporte: bucle con `stop_reason`, `tool_choice`, bloqueo en código y límite de reembolso | Arquitectura agéntica, herramientas |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv
cp .env.example .env   # y pega tu ANTHROPIC_API_KEY en .env
```

## Ejecutar el Lab 1

```bash
cd lab1
python agent.py
```

## Notas

- La clave vive solo en `.env`, que está en `.gitignore`.
- Verifica nombres de modelos, precios y flags contra la documentación
  oficial de Anthropic antes del examen.