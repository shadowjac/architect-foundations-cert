# Architect Foundations: labs

Labs prácticos en Python con el SDK de Anthropic para preparar la
certificación Claude Certified Architect – Foundations (CCAR-F).

## Labs

| Lab | Tema | Dominios que practica |
|---|---|---|
| [lab1](lab1/) | Agente de soporte: bucle con `stop_reason`, `tool_choice`, bloqueo en código y límite de reembolso | Arquitectura agéntica, herramientas |
| [lab2](lab2/) | Investigación multi-agente: coordinador con `tool_choice` forzado, subagentes en paralelo, manejo de errores y síntesis | Arquitectura agéntica, herramientas, fiabilidad |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env   # y pega tu ANTHROPIC_API_KEY en .env
```

## Configuración

- Los ajustes compartidos (modelo, tope de iteraciones) viven en `config.py`.
- La clave de API vive solo en `.env`, que está en `.gitignore`.

## Ejecutar el Lab 1

```bash
cd lab1
python agent.py
```

## Ejecutar el Lab 2

```bash
cd lab2
python run.py
```

## Notas

- Verifica nombres de modelos, precios y flags contra la documentación
  oficial de Anthropic antes del examen.