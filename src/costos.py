from abc import ABC, abstractmethod
from fastapi import FastAPI, APIRouter, Depends

class CalcularKilometros(ABC):
    @abstractmethod
    def calcular_distancia(self, origen, destino):
        pass

class CalcularCuadras:
    def calcular_cuadras(self, origen, destino):
        return abs(origen - destino)

# "Adapter" que convierte cuadras a kilómetros
class Cuadras_a_km(CalcularKilometros):
    def __init__(self, calcularcuadras: CalcularCuadras):
        self.calcularcuadras = calcularcuadras

    def calcular_distancia(self, origen, destino):
        distancia_cuadras = self.calcularcuadras.calcular_cuadras(origen, destino)
        distancia_km = distancia_cuadras / 10
        return distancia_km

# Función para calcular el costo del domicilio basado en la distancia en kilómetros
def calcular_costo(distancia_km):
    base: int = 5000
    excedent: int = 500
    if distancia_km > 3:
        base = base + (excedent*(distancia_km-3))
    return base

api = APIRouter()

# Integración del "Adapter" con el cálculo de costo
@api.get("/delivery-cost")
def calculate_delivery_cost(origen: int, destino: int):
    calcularcuadras = CalcularCuadras()
    adapter = Cuadras_a_km(calcularcuadras)
    distancia_km = adapter.calcular_distancia(origen, destino)
    cost = calcular_costo(distancia_km)
    print(f"Distancia: {distancia_km} km")
    return cost