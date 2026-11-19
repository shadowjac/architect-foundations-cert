import time
from concurrent.futures import ThreadPoolExecutor

import anthropic
from coordinator import plan
from subagent import run_subagent

MAX_WORKERS = 5
MAX_RETRIES = 2  # reintentos extra, con tope
BACKOFF_SECONDS = 1.0


def classify(exc):
    if isinstance(exc, anthropic.APIConnectionError):
        return "transient"
    if isinstance(exc, anthropic.APIStatusError):
        if exc.status_code == 429 or exc.status_code >= 500:
            return "transient"
        return "permanent"  # 400/401/403...: reintentar no arregla nada
    return "permanent"  # bug propio u otro error: no reintentar a ciegas


def safe_run(task):
    attempt = 0
    while True:
        try:
            return run_subagent(task)
        except Exception as exc:
            category = classify(exc)
            if category == "transient" and attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * 2 ** attempt)
                attempt += 1
                continue
            return {"ok": False, "task_id": task["id"],
                    "error": {"category": category,
                              "message": f"{type(exc).__name__}: {exc}",
                              "attempts": attempt + 1}}


def run_subagents(subtasks, parallel=True):
    if not parallel:
        return [safe_run(t) for t in subtasks]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        return list(pool.map(safe_run, subtasks))


def partition(results):
    return {
        "failed": [r for r in results if not r["ok"]],
        "no_sources": [r for r in results if r["ok"] and r.get("no_sources")],
        "answered": [r for r in results if r["ok"] and not r.get("no_sources")],
    }


def run_research(question, parallel=True):
    p = plan(question)
    if not p["in_scope"]:
        return {"in_scope": False, "results": []}
    results = run_subagents(p["subtasks"], parallel)
    return {"in_scope": True, "results": results, **partition(results)}