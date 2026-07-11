from fastapi import FastAPI
import requests
import time

app = FastAPI()


# =========================
# APIs externas
# =========================

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&current_weather=true"
    return requests.get(url, timeout=3).json()


def get_usd_brl():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=BRL"
    return requests.get(url, timeout=3).json()


# =========================
# Endpoint principal
# =========================

@app.get("/process")
def process():

    start = time.time()

    weather = None
    currency = None
    errors = []

    # 🌦️ Weather
    try:
        weather = get_weather()
    except Exception as e:
        errors.append(f"weather_error: {str(e)}")

    # 💱 Currency
    try:
        currency = get_usd_brl()
    except Exception as e:
        errors.append(f"currency_error: {str(e)}")

    duration = time.time() - start

    return {
        "service": "C",
        "status": "ok" if not errors else "partial",
        "latency_sec": round(duration, 3),
        "weather": weather,
        "currency": currency,
        "errors": errors
    }
