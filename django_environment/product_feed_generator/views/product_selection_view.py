from django.template.loader import get_template
from django.http import HttpResponse
import xmltodict
import urllib.request
from urllib.request import Request
import pprint
import json
from dicttoxml import dicttoxml
from product_feed_generator.models import Feed, Serverkast_Product, TopSystemsProduct
from product_feed_generator.forms import *
from product_feed_generator.views.helper import *

def product_selection_view(request, shop_name):
    if "add_products_to_final_feed_submit" in request.POST:
        template = get_template("product_selection_page.html")
        context = add_products_to_final_feed(request, shop_name)
        return HttpResponse(template.render(context, request))
    
    elif "generate_refresh_submit" in request.POST:
        template = get_template("product_selection_page.html")
        context = extract_and_save_products(request, shop_name)
        return HttpResponse(template.render(context, request))

    elif request.method == "GET":
        feed = Feed.objects.get(shop_name=shop_name)
        template = get_template("product_selection_page.html")
        if (shop_name == "Serverkast"):
            current_products = Serverkast_Product.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = { "%s ––– %s"%(row.ean,row.name) : row.is_selected for row in current_products }
            form = ServerkastProductSelectForFinalFeedForm(init)
            context = {
                "feed": feed,
                "form": form,
            }
        elif (shop_name == "TopSystems"):
            current_products = TopSystemsProduct.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = { "%s ––– %s"%(row.ean,row.name) : row.is_selected for row in current_products }
            form = TopSystemsProductSelectForFinalFeedForm(init)
            context = {
                "feed": feed,
                "form": form,
            }
        return HttpResponse(template.render(context, request))
