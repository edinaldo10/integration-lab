from fastapi import FastAPI, HTTPException, Request
from prometheus_fastapi_instrumentator import Instrumentator
import os, random, time, json
from datetime import datetime
from resilience import service_c_breaker # Seu disjuntor

app = FastAPI()

# 1. Inicializa o Instrumentator (MANTIDO)
Instrumentator().instrument(app).expose(app)

FAIL_MODE = os.getenv("FAIL_MODE", "false").lower() == "true"

# 2. Função de Log estruturado (MANTIDO)
def log_event(level, msg, trace_id=None):
    log_data = {
        "ts": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "level": level,
        "msg": msg,
        "trace_id": trace_id
    }
    print(json.dumps(log_data))

@app.get("/process")
def process(request: Request):
    # Captura o Trace ID que vem do Serviço A
    trace_id = request.headers.get("X-Trace-Id", "no-trace-id")
    
    # 3. Simulação de Fail Mode (MANTIDO)
    if FAIL_MODE:
        log_event("ERROR", "Falha forçada via FAIL_MODE", trace_id)
        return {"service": "B", "status": "error", "reason": "forced failure"}

    # 4. Proteção com Circuit Breaker envolvendo a lógica de simulação
    try:
        def simulacao_chamada_c():
            # Aqui mantém-se a falha aleatória para testar a resiliência
            if random.random() < 0.2:
                raise Exception("Falha aleatória no Serviço C")
            time.sleep(random.uniform(0.2, 2.0))
            return {"status": "ok", "service": "C"}

        # O Circuit Breaker gerencia a chamada acima
        result = service_c_breaker.call(simulacao_chamada_c)
        return {"service": "B", "status": "ok", "downstream": result}

    except Exception:
        # Quando o disjuntor abre ou a simulação falha
        log_event("WARNING", "Circuit Breaker abriu ou Serviço C falhou - Modo Fallback", trace_id)
        return {"service": "B", "status": "fallback", "msg": "Serviço indisponível, usando cache"}
