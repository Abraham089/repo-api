from fastapi import APIRouter, HTTPException
from ...models.woo import RequestedCustomer
from repo_api_equipo_e.services.woo import create_customer
from starlette import status

router = APIRouter()

@router.post("/customer", status_code=status.HTTP_201_CREATED)
def create_order(customerList: list[RequestedCustomer]):
    results = []
    for customer in customerList:
        try:
            new_customer = create_customer(customer)
            results.append({"email": customer.email, "status": "success", "data": new_customer})
        except Exception as e:
            results.append({"email": customer.email, "status": "error", "message": str(e)})

    return results
