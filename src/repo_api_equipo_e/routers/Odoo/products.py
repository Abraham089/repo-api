from fastapi import APIRouter
from repo_api_equipo_e.services.odoo import fetch_odoo_products, create_odoo_products
from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/products")
def get_products():
    return fetch_odoo_products()

@router.post("/products")
def create_products():
    new_products = [
        {'name': 'Teclado Mecánico Custom 60%', 'list_price': 125.0, 'type': 'product', 'qty': 15, 'categ_id': 1},
        {'name': 'Mouse Gamer 26K DPI', 'list_price': 79.99, 'type': 'product', 'qty': 20, 'categ_id': 1},
        {'name': 'Monitor Gamer Curvo 27"', 'list_price': 299.50, 'type': 'product', 'qty': 8, 'categ_id': 1},
        {'name': 'Gabinete para SSD NVMe M.2', 'list_price': 28.50, 'type': 'product', 'qty': 16, 'categ_id': 1},
        {'name': 'Hub USB-C 8 en 1 Aluminio', 'list_price': 55.0, 'type': 'product', 'qty': 18, 'categ_id': 1},

        {'name': 'Audífonos de Estudio Abiertos', 'list_price': 160.0, 'type': 'product', 'qty': 12, 'categ_id': 2},
        {'name': 'Micrófono Dinámico XLR', 'list_price': 199.0, 'type': 'product', 'qty': 6, 'categ_id': 2},
        {'name': 'Interfaz de Audio USB-C', 'list_price': 145.0, 'type': 'product', 'qty': 10, 'categ_id': 2},
        {'name': 'Cámara Streamer 4K Pro', 'list_price': 110.0, 'type': 'product', 'qty': 7, 'categ_id': 2},

        {'name': 'Silla Ejecutiva Mesh Transpirable', 'list_price': 185.0, 'type': 'product', 'qty': 5, 'categ_id': 3},
        {'name': 'Descansapiés Ergonómico Ajustable', 'list_price': 40.0, 'type': 'product', 'qty': 12, 'categ_id': 3},
        {'name': 'Pizarra Blanca de Vidrio 90x60', 'list_price': 75.0, 'type': 'product', 'qty': 4, 'categ_id': 3},

        {'name': 'Brazo Articulado para Micrófono', 'list_price': 45.0, 'type': 'product', 'qty': 25, 'categ_id': 4},
        {'name': 'Barra de Luz LED para Monitor', 'list_price': 38.0, 'type': 'product', 'qty': 30, 'categ_id': 4},
        {'name': 'Tapete de Escritorio Fieltro XL', 'list_price': 24.99, 'type': 'product', 'qty': 40, 'categ_id': 4},
        {'name': 'Cargador GaN 100W de Pared', 'list_price': 49.0, 'type': 'product', 'qty': 22, 'categ_id': 4},
        {'name': 'Soporte Vertical Doble para Laptop', 'list_price': 32.0, 'type': 'product', 'qty': 14, 'categ_id': 4},
        {'name': 'Organizador de Cables Magnético', 'list_price': 15.0, 'type': 'product', 'qty': 50, 'categ_id': 4},
        {'name': 'Memoria MicroSD 256GB Evo', 'list_price': 35.0, 'type': 'product', 'qty': 35, 'categ_id': 4},
        {'name': 'Tira LED RGB Inteligente 5m', 'list_price': 20.0, 'type': 'product', 'qty': 45, 'categ_id': 4},
    ]
    execution_report = create_odoo_products(new_products)

    if len(execution_report["errors"]) == len(new_products):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Ningún producto pudo ser procesado.", "errors": execution_report["errors"]}
        )
    
    if len(execution_report["errors"]) > 0:
        return {
            "status": "partial_success",
            "message": "Sincronización terminada con algunos errores.",
            "data": execution_report
        }
    
    return {
        "status": "success",
        "message": "Todos los productos han sido procesados de manera impecable.",
        "data": execution_report
    }