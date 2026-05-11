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

@router.get("/coupons/code/{coupon_code}")
def get_coupon_by_code(coupon_code: str):
  response = wcapi.get(
        "coupons",
        params={"code": coupon_code}
    )
  
  coupons = response.json()

  if not coupons:
    raise HTTPException(status_code=404, detail="Cupón no encontrado")
  
  coupon = coupons[0]  # Asumimos que el código de cupón es único y tomamos el primero

  if response.status_code == 200:
    print(f"Code: {coupon['code']} | ID: {coupon['id']} | Tipo: {coupon['discount_type']} | Importe: ${coupon['amount']} | Descripción: {coupon['description']}")

  else:
    print(f"Error {response.status_code}: {response.text}")


  return coupon