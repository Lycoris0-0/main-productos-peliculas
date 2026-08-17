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

class Pelicula(BaseModel):
    id: int | None = None
    nombre: str
    valoracion: float | None = None
    genero: str

class PeliculaCreate(BaseModel):
    nombre: str
    valoracion: float | None = None
    genero: str
# ENDPOINTS
# GET
@app.get("/peliculas")
async def obtenerPelicula() -> list[Pelicula]:
    conexion = sqlite3.connect("vista_peliculas.db")
    conexion.row_factory = sqlite3.Row

    cursor = conexion.cursor()

    respuesta = cursor.execute(f"SELECT * FROM peliculas")

    return [dict(pelicula) for pelicula in respuesta.fetchall()]
# POST
@app.post("/peliculas")
async def agregarPelicula(pelicula: PeliculaCreate):
    conexion = sqlite3.connect("vista_peliculas.db")
    
    cursor = conexion.cursor()
    
    print(pelicula.nombre)
    print(pelicula.valoracion)
    print(pelicula.genero) 

    cursor.execute("INSERT INTO peliculas VALUES(?, ?, ?, ?)", (None,pelicula.nombre,pelicula.valoracion, pelicula.genero))

    conexion.commit()

    conexion.close()

# PUT

# PATCH



# DELETE
