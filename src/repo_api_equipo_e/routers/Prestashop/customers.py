import os
import httpx
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()

BASE_URL = os.getenv("PRESTASHOP_BASE_URL", "").rstrip("/")
API_KEY = os.getenv("PRESTASHOP_API_KEY", "")


@router.get("/customers")
async def get_customers():

    if not BASE_URL or not API_KEY:
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": "500",
                    "message": "PrestaShop no configurado - falta BASE_URL o API_KEY"
                }
            ]
        }

    try:
        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/api/customers"
            logger.debug(f"Requesting: {url}")
            
            r = await client.get(
                url,
                params={
                    "ws_key": API_KEY,
                    "display": "full",
                    "output_format": "JSON"
                }
            )

        if r.status_code != 200:
            logger.error(f"PrestaShop API error: {r.status_code} - {r.text}")
            return {
                "status": "error",
                "data": None,
                "errors": [
                    {
                        "code": str(r.status_code),
                        "message": f"Error al consultar PrestaShop: {r.text[:200]}"
                    }
                ]
            }
    except Exception as e:
        logger.error(f"Exception calling PrestaShop: {e}")
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": "500",
                    "message": f"Error de conexión: {str(e)}"
                }
            ]
        }
    
    data = r.json()

    if isinstance(data, list):
        customers = data
    else:
        customers = data.get("customers", [])

    if not customers:
        return {
            "status": "error",
            "data": None,
            "errors": [
                {
                    "code": "404",
                    "message": "Cliente no encontrado"
                }
            ]
        }
    
    cleaned_customers = []
    for customer in customers:
        composed_name = customer.get("name", "")
        name = composed_name[0].get("value") if isinstance(composed_name, list) else composed_name
        
        cleaned_customers.append({
            "id": customer.get("id"),
            "nombre": customer.get("firstname"),
            "apellido": customer.get("lastname"),
            "passwd": customer.get("passwd"),
            "email": customer.get("email")
        })

    # SUCCESS
    return {
        "status": "success",
        "data": cleaned_customers,
        "errors": []
    }