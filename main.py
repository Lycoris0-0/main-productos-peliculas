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
@app.post("/productos")
async def agregarProducto(producto: ProductoCreate):
    conexion = sqlite3.connect("master.db")
    
    cursor = conexion.cursor()
    
    print(producto.nombre)
    print(producto.precio) 

    cursor.execute("INSERT INTO productos VALUES(?, ?, ?)", (None,producto.nombre, producto.precio))

    conexion.commit()

    conexion.close()


# PATCH

# PUT

# DELETE
