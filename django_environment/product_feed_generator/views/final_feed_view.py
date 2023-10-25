from django.template.loader import get_template
from django.http import HttpResponse
import xmltodict
import urllib.request
from urllib.request import Request
import json
from product_feed_generator.models import Serverkast_Product
from dicttoxml import dicttoxml

def final_feed_view(request):
    if "generate_final_feed_submit" in request.POST:
        """
            TODO-FFC
            GET SELECTED PRODUCTS
            FROM ALL FEEDS
            NOT JUST Serverkast_Product
        """
        products = Serverkast_Product.objects.filter(is_selected=True).values()
        xml = dicttoxml(products, custom_root='test', attr_type=False)
        f =  open("product_feed_generator/templates/final-feed-file.xml", "wb")
        f.write(xml)
        f.close()
        context = {"message": 'File is generated.'}
        template = get_template("final_feed_page.html")
        return HttpResponse(template.render(context, request))
    elif request.method == "GET":
        context = {}
        template = get_template("final_feed_page.html")
        return HttpResponse(template.render(context, request))