from fastapi import APIRouter
from repo_api_equipo_e.services.woo import get_woo_customers

router = APIRouter()

@router.get("/customers")
def obtain_customers():
  return get_woo_customers()