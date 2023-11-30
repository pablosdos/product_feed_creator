from decimal import Decimal

def apply_topsystems_configuration_scheme(complete_topsystems_products_list):
    for product in complete_topsystems_products_list:
        product['retail_price_excluding_tax'] = round(( product.get('sales_price_excluding_tax')  / 121 ) * 100, 2)
        product['cost_price'] = round(product.get('retail_price_excluding_tax') * Decimal(0.65), 2)
    return complete_topsystems_products_list

def apply_serverkast_configuration_scheme(complete_serverkast_products_list):
    for product in complete_serverkast_products_list:
        product['retail_price_excluding_tax'] = round( product.get('sales_price_excluding_tax')* Decimal(1.15), 2)
        product['cost_price'] = round(product.get('sales_price_excluding_tax') * Decimal(0.85), 2)
    return complete_serverkast_products_list

