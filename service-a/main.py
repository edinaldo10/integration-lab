import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

SERVICE_B_URL = os.getenv("SERVICE_B_URL")

@app.get("/start")
def start():
    try:
        # Aumentamos o timeout para não travar o Service A
        r = requests.get(f"{SERVICE_B_URL}/process", timeout=3)
        
        # Se o Service B responder com erro (4xx ou 5xx), levantamos uma exceção
        r.raise_for_status()
        
        return {
            "service": "A",
            "status": "ok",
            "downstream": r.json()
        }
    except requests.exceptions.RequestException as e:
        # Aqui capturamos erros de conexão ou erros HTTP do Service B
        return {
            "service": "A",
            "status": "fallback",
            "message": "Service B indisponível ou em erro",
            "details": str(e)
        }
