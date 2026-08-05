from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
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
    return { "Estado": "Servidor en línea"}

# MODELOS
class Producto(BaseModel):
    id: int | None = None
    nombre: str
    precio: int

class ProductoCreate(BaseModel):
    nombre: str
    precio: int

# ENDPOINTS
# GET
@app.get("/productos")
async def obtenerProductos() -> list[Producto]:
    conexion = sqlite3.connect("master.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute(f"SELECT * FROM productos")

    return [dict(producto) for producto in respuesta.fetchall()]
# POST

# PATCH

# PUT

# DELETE
