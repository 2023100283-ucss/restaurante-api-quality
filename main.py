from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

class Item(BaseModel):
    id: int
    nombre: str
    precio: float
    cantidad: int

class Pedido(BaseModel):
    usuario_id: str
    items: List[Item]
    direccion: str

# SIMULACIÓN DE BASE DE DATOS
def get_db_connection():
    conn = sqlite3.connect('restaurante.db')
    return conn

@app.post("/crear-pedido")
async def crear_pedido(pedido: Pedido):
    # --- MÉTRICA INTERNA: COMPLEJIDAD CICLOMÁTICA ALTA ---
    # Demasiados IFs anidados para validar reglas de negocio
    if pedido.usuario_id:
        if len(pedido.items) > 0:
            total = 0
            for item in pedido.items:
                if item.cantidad > 0:
                    if item.precio > 0:
                        total += item.precio * item.cantidad
                    else:
                        raise HTTPException(status_code=400, detail="Precio inválido")
                else:
                    raise HTTPException(status_code=400, detail="Cantidad debe ser mayor a 0")
            
            # --- MÉTRICA DE SEGURIDAD: SQL INJECTION (Vulnerabilidad) ---
            # Inyección intencional usando f-strings en lugar de parámetros
            conn = get_db_connection()
            cursor = conn.cursor()
            query = f"INSERT INTO pedidos (usuario, total) VALUES ('{pedido.usuario_id}', {total})" 
            cursor.execute(query) # <--- Sonar detectará esto como Crítico
            conn.commit()
            conn.close()
            
            return {"status": "Pedido creado", "total": total}
        else:
            raise HTTPException(status_code=400, detail="El pedido está vacío")
    else:
        raise HTTPException(status_code=400, detail="Usuario no identificado")

# --- CODE SMELL: FUNCIÓN NO UTILIZADA ---
def funcion_obsoleta_que_nadie_borro():
    pass