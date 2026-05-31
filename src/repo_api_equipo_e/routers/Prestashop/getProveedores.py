import os
import httpx
from fastapi import APIRouter

router = APIRouter()

BASE_URL = os.getenv("PRESTASHOP_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("PRESTASHOP_API_KEY", "")


@router.get("/proveedores")
async def getProveedores():

    if not BASE_URL or not API_KEY:
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": "500",
                    "message": "PrestaShop no configurado"
                }
            ]
        }

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/api/suppliers",
            params={
                "ws_key": API_KEY,
                "display": "full",
                "output_format": "JSON"
            }
        )

    if r.status_code != 200:
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": str(r.status_code),
                    "message": "Error al consultar PrestaShop"
                }
            ]
        }
    
    data = r.json()

    if isinstance(data, list):
        proveedores = data
    else:
        proveedores = data.get("proveedores", [])

    if not proveedores:
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": "404",
                    "message": "Proveedores no encontrados"
                }
            ]
        }

    return {
        "status": "success",
        "data": proveedores[0],
        "errors": []
    }