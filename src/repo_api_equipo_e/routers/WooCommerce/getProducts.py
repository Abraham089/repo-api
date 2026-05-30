from fastapi import APIRouter, HTTPException
from repo_api_equipo_e.services.odoo import fetch_odoo_products
from woocommerce import API
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

wcapi = API(
    url=os.getenv("WC_URL"),
    consumer_key=os.getenv("WC_CONSUMER_KEY"),
    consumer_secret=os.getenv("WC_CONSUMER_SECRET"),
    version="wc/v3",
    timeout=20
)

    
@router.get("/products")
def get_woo_products():
    response = wcapi.get("products", params={"per_page": 10, "fields": "name,id,description,price"})

    if response.status_code == 200:
        productos = response.json()
        print(f"--- Se encontraron {len(productos)} productos ---")

        # Filtrar solo los campos especificados
        campos = ["id", "name", "description", "price"]
        productos_filtrados = [
            {campo: p.get(campo) for campo in campos if campo in p}
            for p in productos
        ]

        for p in productos_filtrados:
            print(f"ID: {p['id']} | Nombre: {p['name']} | Descripción: {p['description']} | Precio: ${p['price']}")
        return productos_filtrados
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

@router.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
   
    response = wcapi.get(f"customers/{customer_id}")

    if response.status_code == 200:
        customer = response.json()
        print(f"--- Cliente encontrado: {customer['id']} | Nombre: {customer['first_name']} {customer['last_name']} ---")
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return customer