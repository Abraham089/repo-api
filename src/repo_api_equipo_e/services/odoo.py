from repo_api_equipo_e.odoo import connect_odoo

def fetch_odoo_products():
    uid, models, db, password = connect_odoo()

    products = models.execute_kw(
        db, uid, password,
        "product.product", "search_read",
        [[]],
        {"fields": ["id", "name", "default_code", "list_price", "categ_id"]}
    )

    return products

def create_odoo_products(new_products):
    uid, models, db, password = connect_odoo()
    
    report = {
        "created": [],
        "already_existed": [],
        "errors": []
    }
    
    for p in new_products:
        name = p.get('name', 'Producto Sin Nombre')
        try:
            cantidad = p.get('qty')
            
            existing_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[('name', '=', name)]])
            
            if existing_ids:
                product_id = existing_ids[0]
                report["already_existed"].append(name)
                print(f"'{name}' ya existe (ID: {product_id}).")
            else:
                clean_data = {k: v for k, v in p.items() if k != 'qty'}
                product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [clean_data])
                report["created"].append(name)
                print(f"Creado: {name} (ID: {product_id} | Categoría: {clean_data['categ_id']})")
            
            try:
                quant_id = models.execute_kw(db, uid, password, 'stock.quant', 'create', [{
                    'product_id': product_id,
                    'location_id': 8, 
                    'inventory_quantity': cantidad,
                }])
                models.execute_kw(db, uid, password, 'stock.quant', 'action_apply_inventory', [[quant_id]])
                print(f"Stock de {cantidad} aplicado.")
            except TypeError as te:
                if "cannot marshal None" in str(te):
                    print(f"Stock de {cantidad} aplicado (Odoo respondió con None).")
                else:
                    raise te

        except Exception as e:
            error_msg = f"Error en '{name}': {str(e)}"
            report["errors"].append(error_msg)
            print(error_msg)

    return report