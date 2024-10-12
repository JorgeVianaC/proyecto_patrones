from fastapi import FastAPI, APIRouter
import psycopg2
from typing import List
from decimal import Decimal


connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",
    database="Domis",
    port="5432"
)
connection.autocommit = True

def crearTabla():
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS trayecto(
        ID SERIAL PRIMARY KEY, 
        origen NUMERIC(10), 
        destino NUMERIC(10), 
        km NUMERIC(10,2), 
        costo NUMERIC(10,2), 
        metodo_pago VARCHAR(30))
    """
    cursor.execute(query)
    cursor.close()
    
api = APIRouter()
@api.get("/trayectos")
def consultarTabla():
    cursor = connection.cursor()
    query = "SELECT * FROM trayecto"
    cursor.execute(query)
    result = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas
    trayectos = ""
    for fila in result:
        registro = []
        for columna, valor in zip(columnas, fila):  # Convertir Decimal a float si es necesario, ya que la funcion devuelve valores tipo numeric
            if isinstance(valor, Decimal):
                valor = float(valor)
            registro.append(f"{columna}: {valor}")
        trayectos += ", ".join(registro) + "\n  "
    return trayectos

def insertar_datos(origen: int, destino: int, km: int, costo: int, metodo_pago: str):
    cursor = connection.cursor()
    query = f" INSERT INTO trayecto(origen, destino, km, costo, metodo_pago) values (%s, %s, %s, %s, %s) "
    cursor.execute(query,(origen, destino, km, costo, metodo_pago))
    cursor.close()
    
def eliminarTabla():
    cursor = connection.cursor()
    query = "DROP TABLE IF EXISTS trayecto"
    cursor.execute(query)
    cursor.close()

#crearTabla()
#consultarTabla()