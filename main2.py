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
    return { "Estado": "Servidor en línea"}

class Factura(BaseModel):
    id:  int | None = None
    numero_factura: int
    fecha: int
    cliente: str
    total:int

class FacturaCreate(BaseModel):
    numero_factura: int
    cliente
