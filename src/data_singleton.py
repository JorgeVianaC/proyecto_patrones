from fastapi import FastAPI, APIRouter
import psycopg2
from psycopg2 import OperationalError
from decimal import Decimal
from sqlalchemy import create_engine, text, Column, Integer, Numeric, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator, Optional, List, Any

class Database:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            print("Creating Database instance")
            DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
                "postgres",
                "postgres",
                "localhost",
                "5432",
                "Domis"
            )
            cls.instance = super().__new__(cls)
            cls.instance.engine = create_engine(DATABASE_URL)
            cls.instance.session = sessionmaker(autocommit=False, autoflush=False, bind=cls.instance.engine)
        print("Database instance already created")
        return cls.instance
    
    def execute_query(self, query: str) -> Optional[List[Any]]:
        with self.engine.connect() as connection:
            # Usa text() para ejecutar la consulta
            result = connection.execute(text(query))
            # Devuelve resultados si la consulta es de tipo SELECT
            if query.strip().lower().startswith("select"):
                return result.fetchall()
            return None

def get_db() -> Generator[Session, None, None]:
    db = Database()
    db_session = db.session()  # type: ignore
    try:
        yield db_session
    finally:
        db_session.close()
        
Base = declarative_base()

class Trayecto(Base):
    __tablename__ = 'trayecto'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    origen = Column(Numeric(10), nullable=False)
    destino = Column(Numeric(10), nullable=False)
    km = Column(Numeric(10, 2), nullable=False)
    costo = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(String(30), nullable=False)
        
def crearTabla():
    query = """
    CREATE TABLE IF NOT EXISTS trayecto(
        ID SERIAL PRIMARY KEY, 
        origen NUMERIC(10), 
        destino NUMERIC(10), 
        km NUMERIC(10,2), 
        costo NUMERIC(10,2), 
        metodo_pago VARCHAR(30))
    """
    db = Database()
    db.execute_query(query)

def insertar_datos(origen: int, destino: int, km: int, costo: int, metodo_pago: str):
    db = Database()
    with db.session() as session:  # Usa la sesión para insertar datos
        nuevo_trayecto = Trayecto(
            origen=origen,
            destino=destino,
            km=km,
            costo=costo,
            metodo_pago=metodo_pago
        )
        session.add(nuevo_trayecto)  # Agrega el nuevo registro a la sesión
        session.commit()  # Realiza el commit para guardar los cambios
        
crearTabla()
