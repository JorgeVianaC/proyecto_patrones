from abc import ABC, abstractmethod
from fastapi import FastAPI, APIRouter, HTTPException
from src.costos import calcular_costo, Cuadras_a_km, CalcularCuadras
from src.data import insertar_datos
from typing import Literal

# Interfaz Strategy
class MetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto):
        pass

# Estrategia de Pago en Efectivo
class PagoEfectivo(MetodoPago):
    def procesar_pago(self, monto):
        return {"método": "Efectivo", "monto": monto}

# Estrategia de Pago de Transferencia
class PagoTransferencia(MetodoPago):
    def procesar_pago(self, monto):
        return {"método": "Transferencia", "monto": monto}
        
# Clase de Contexto para el Pago
class ContextoPago:
    def __init__(self, strategy: MetodoPago):
        self._strategy = strategy

    def procesar_pago(self, monto):
        return self._strategy.procesar_pago(monto)

api = APIRouter()

@api.get("/pago")
def procesar_pago(origen: int, destino: int, metodo: Literal["efectivo", "transferencia"]):
    # Calcula desde costos.py
    
    calcularcuadras = CalcularCuadras()
    adapter = Cuadras_a_km(calcularcuadras)
    distancia_km = adapter.calcular_distancia(origen, destino)
    monto = calcular_costo(distancia_km)
    
    # factory
    if metodo == "efectivo":
        m_pago: str = 'efectivo'
        estrategia_pago = PagoEfectivo()
    elif metodo == "transferencia":
        m_pago: str = 'transferencia'
        estrategia_pago = PagoTransferencia()
    else:
        return {"error": "Método de pago no válido. Use 'efectivo' o 'transferencia'."}
    
    insertar_datos(origen, destino, distancia_km, monto, m_pago)
    
    # Crear el contexto con la estrategia seleccionada y procesar el pago
    contexto_pago = ContextoPago(estrategia_pago)
    return contexto_pago.procesar_pago(monto)
