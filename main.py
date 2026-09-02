from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/obtenerCedula")
def obtener_cedula():
    cedula = random.randint(1_000_000_000, 9_999_999_999)
    return {"cedula": cedula}
