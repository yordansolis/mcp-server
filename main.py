from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Simulación de base de datos
RECORDS = [
    {
        "id": "1",
        "title": "Cupcake de chocolate",
        "text": "Pedido de 12 cupcakes de chocolate con chispas",
        "metadata": {"cliente": "Carlos", "fecha": "2025-06-01"},
        "url": "https://example.com/pedido/1"
    },
    {
        "id": "2",
        "title": "Cupcake de vainilla",
        "text": "Pedido urgente de cupcakes sabor vainilla para evento",
        "metadata": {"cliente": "Ana", "fecha": "2025-06-15"},
        "url": "https://example.com/pedido/2"
    },
]

# Crear diccionario de lookup por ID
LOOKUP = {r["id"]: r for r in RECORDS}

# Modelos de entrada/salida para FastAPI
class SearchInput(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: str
    title: str
    text: str
    url: Optional[str] = None

class SearchOutput(BaseModel):
    results: List[SearchResult]

class FetchInput(BaseModel):
    id: str

class FetchOutput(BaseModel):
    id: str
    title: str
    text: str
    url: Optional[str]
    metadata: Optional[dict]

# Crear instancia FastAPI con documentación clara
app = FastAPI(
    title="Servidor de pedidos de cupcakes",
    description="API para buscar y recuperar pedidos de cupcakes mediante herramientas de búsqueda.",
    version="1.0.0"
)

# 🔍 Endpoint de búsqueda
@app.post("/tools/search", response_model=SearchOutput, summary="Buscar pedidos de cupcakes")
async def search_tool(input: SearchInput):
    """
    Busca pedidos de cupcakes que coincidan con las palabras clave ingresadas.
    Busca coincidencias en el título, descripción y metadatos del pedido.
    """
    query = input.query.lower().split()
    results = []

    for r in RECORDS:
        texto_completo = " ".join([
            r.get("title", ""),
            r.get("text", ""),
            " ".join(r.get("metadata", {}).values()) # metadata sirve como diccionario de palabras clave/valor
        ]).lower()

        if any(palabra in texto_completo for palabra in query):
            results.append({
                "id": r["id"],
                "title": r["title"],
                "text": r["text"],
                "url": r.get("url")
            })

    return {"results": results}

# 📄 Endpoint para recuperar detalles por ID
@app.post("/tools/fetch", response_model=FetchOutput, summary="Obtener detalles de un pedido")
async def fetch_tool(input: FetchInput):
    """
    Recupera todos los detalles de un pedido de cupcakes a partir de su ID.
    """
    if input.id not in LOOKUP:
        raise ValueError("ID no encontrado")

    r = LOOKUP[input.id]
    return {
        "id": r["id"],
        "title": r["title"],
        "text": r["text"],
        "url": r.get("url"),
        "metadata": r.get("metadata", {})
    }

# 🔁 Ejecutar el servidor
if __name__ == "__main__":
    uvicorn.run("cupcake_server:app", host="0.0.0.0", port=8000, reload=True)
