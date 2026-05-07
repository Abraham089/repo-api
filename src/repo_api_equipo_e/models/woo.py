from pydantic import BaseModel, Field
from typing import List

class BillingInfo(BaseModel):
   address_1: str = Field(min_length=1)
   city: str = Field(min_length=1)
   country: str = Field(min_length=1)
   model_config = {
     "json_schema_extra": {
        "example": {
          "billing": {
              "address_1": "354 calle de ejemplo",
              "city": "ciudad de ejemplo",
              "country": "pais de ejemplo"
              }
          }
      }
    }

class ShippingInfo(BaseModel):
   address_1: str = Field(min_length=1)
   city: str = Field(min_length=1)
   country: str = Field(min_length=1)

   model_config = {
     "json_schema_extra": {
        "example": {
          "shipping": {
              "address_1": "354 calle de ejemplo",
              "city": "ciudad de ejemplo",
              "country": "pais de ejemplo"
              }
          }
      }
    }

class LineItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class RequestedOrder(BaseModel):
  payment_method: str = Field(min_length=1)
  payment_method_title: str = Field(min_length=1)
  set_paid: bool
  billing: BillingInfo
  line_items: List[LineItem] = Field(min_items=1)

  model_config = {
     "json_schema_extra": {
        "example": {
          "payment_method": "metodo de ejemplo",
          "payment_method_title": "titulo de ejemplo",
          "set_paid": True,
          "billing": {
              "first_name": "Nombre de ejemplo",
              "last_name": "Apellido de ejemplo",
              "email": "alguien@ejemplo.com"
              },
          "line_items": [{"product_id": 1, "quantity": 1}]
          }
      }
    }

class RequestedCustomer(BaseModel):
  first_name: str = Field(min_length=1)
  last_name: str = Field(min_length=1)
  email: str = Field(min_length=1)
  billing: BillingInfo
  shipping: ShippingInfo

  model_config = {
     "json_schema_extra": {
        "example": {
          "first_name": "nombre de ejemplo",
          "last_name": "apellido de ejemplo",
          "email": "ejemplo@algo.com",
          "billing": {
              "address_1": "354 calle de ejemplo",
              "city": "ciudad de ejemplo",
              "country": "pais de ejemplo"
              },
          "shipping": {
              "address_1": "354 calle de ejemplo",
              "city": "ciudad de ejemplo",
              "country": "pais de ejemplo"
              }
          }
      }
    }