#cosa de prueba eh falsa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return { "palo": "palo"}



# FACTURA

class Factura(BaseModel):
    id: int | None = None
    numero_factura: int
    fecha: str
    cliente: str
    total: int

class FacturaCreate(BaseModel):
    numero_factura: int
    fecha: str
    cliente: str
    total: int


@app.get("/facturas")
async def obtenerFacturas() -> list[Factura]:
    conexion = sqlite3.connect("master.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()

    respuesta = cursor.execute("SELECT * FROM facturas ORDER BY fecha DESC")

    data = respuesta.fetchall()

    conexion.close()

    return [dict(factura) for factura in data]


@app.get("/facturas/{id}")
async def buscarFactura(id: int):
    conexion = sqlite3.connect("master.db")
    conexion.row_factory = sqlite3.Row
    
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM facturas WHERE id = ?", (id,))
    respuesta = cursor.fetchall()

    conexion.commit()
    
    conexion.close()

    if respuesta is None:
        return {"error": "Factura no encontrada"}
            
    return (respuesta)



@app.post("/facturas")
async def agregarFactura(factura: FacturaCreate):
    conexion = sqlite3.connect("master.db")
    
    cursor = conexion.cursor()
    
    print(factura.numero_factura)
    print(factura.cliente) 

    cursor.execute("INSERT INTO facturas VALUES(?, ?, ?, ?,?)", (None, factura.numero_factura, factura.fecha, factura.cliente, factura.total))

    conexion.commit()

    conexion.close()
    return { "mensaje": "Creado correctamente"}

