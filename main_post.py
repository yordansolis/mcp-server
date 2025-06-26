import httpx  # asegúrate de instalarlo con: pip install httpx
from pydantic import BaseModel
from fastapi import FastAPI
from typing import List, Optional


EXTERNAL_URL = "https://api.sampleapis.com/simpsons/characters"


class SearchInput(BaseModel):
    query: str
class SearchResult(BaseModel):
    id: str
    name: str
    normalized_name: str
    gender: Optional[str] = None

class SearchOutput(BaseModel):
    results: List[SearchResult]

app = FastAPI(
    name="Servidor de pedidos de cupcakes",
    description="API para buscar y recuperar pedidos de cupcakes mediante herramientas de búsqueda.",
    version="1.0.0"
)




@app.post("/tools/search", response_model=SearchOutput, summary="Buscar pedidos desde una API externa")
async def search_tool(input: SearchInput):
    """
    Busca pedidos de cupcakes desde una API externa según las palabras clave.
    """
    print("Input:", input)
    async with httpx.AsyncClient() as client:
        response = await client.get(EXTERNAL_URL)
        data = response.json()  # Esto reemplaza RECORDS

        # print(data)

    query = input.query.lower().split()
    results = []

    for r in data:
        normalized_nameo_completo = " ".join([
            r.get("name", ""),
            r.get("normalized_name", ""),
            " ".join(r.get("metadata", {}).values())
        ]).lower()

        if any(palabra in normalized_nameo_completo for palabra in query):
            results.append({
                "id": r["id"],
                "name": r["name"],
                "normalized_name": r["normalized_name"],
                "gender": r.get("gender")
            })

    return {"results": results}
