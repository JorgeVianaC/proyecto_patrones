from fastapi import FastAPI
from src.costos import api as api_costo
from src.pagos import api as api_pago
from src.data import api as api_data, crearTabla

app = FastAPI()
crearTabla()

app.include_router(api_costo, prefix="/costos", tags=["costos"])
app.include_router(api_pago, prefix="/pagos", tags=["pagos"])
app.include_router(api_data, prefix="/data", tags=["data"])

@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}

#Strategy, Adapter, Patrón de Inyección de Dependencias (DI) (no sabía que existia).