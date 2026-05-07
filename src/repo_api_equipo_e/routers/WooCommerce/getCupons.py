from urllib import response

from fastapi import APIRouter, HTTPException
from requests import models
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

    
@router.get("/cupons")
def get_woo_cupons():
    
    response = wcapi.get("coupons", params={"per_page": 10})

    if response.status_code == 200:
        cupones = response.json()
        print(f"--- Se encontraron {len(cupones)} cupones ---")

        for c in cupones:
            print(f"ID: {c['id']} | Nombre: {c['name']} | Codigo: {c['code']} | Descuento: {c['amount']} | Tipo: {c['discount_type']} | Fecha de expiracion: {c['date_expires']}")
    else:
        print(f"Error {response.status_code}: {response.text}")


    return response.json()