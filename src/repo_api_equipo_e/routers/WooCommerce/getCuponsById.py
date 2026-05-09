from urllib import response

from fastapi import APIRouter, HTTPException
from requests import models
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

@router.get("/coupons/{coupon_id}")
def get_coupon_by_id(coupon_id: int):
  response = wcapi.get(f"cupons/{coupon_id}")

  if response.status_code == 200:
    print(f"ID: {response.json()['id']} | Tipo: {response.json()['type']} | Importe: ${response.json()['amount']} | Descripción: {response.json()['description']}")

  else:
    print(f"Error {response.status_code}: {response.text}")


  return response.json()