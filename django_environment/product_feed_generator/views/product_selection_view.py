from django.template.loader import get_template
from django.http import HttpResponse
import xmltodict
import urllib.request
from urllib.request import Request
import pprint
import json
from dicttoxml import dicttoxml
from product_feed_generator.models import Feed, Serverkast_Product
from product_feed_generator.forms import *


def product_selection_view(request, shop_name):
    if "add_products_to_final_feed_submit" in request.POST:
        """
            TODO-FFC (Final Feed Creator)
            GET SELECTED PRODUCTS
            FROM ALL FEEDS
            NOT JUST Serverkast_Product
            AND ADD PRODUCTS
            NOT JUST OVERWRITE
        """
        form = ProductSelectForFinalFeedForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                product_name_of_form = key.split(' ––– ')[1]
                Serverkast_Product.objects.filter(name=product_name_of_form).update(is_selected=value)
        feed = Feed.objects.get(shop_name=shop_name)
        all_updated_products = Serverkast_Product.objects.all()
        template = get_template("product_selection_page.html")
        # has to be identical to field in product_feed_generator/forms/product_select_for_final_feed_form.py
        init = { "%s ––– %s"%(row.ean,row.name) : row.is_selected for row in all_updated_products }
        form = ProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "products": all_updated_products,
            "form": form,
            "message": 'Products are added to Final Feed'
        }
        template = get_template("product_selection_page.html")
        selected_products_from_database = Serverkast_Product.objects.filter(is_selected=True).values()
        xml = dicttoxml(selected_products_from_database, custom_root='product_final_feed', attr_type=False)
        f =  open("product_feed_generator/templates/final-feed-file.xml", "wb")
        f.write(xml)
        f.close()
        return HttpResponse(template.render(context, request))
    
    elif "generate_refresh_submit" in request.POST:
        feed = Feed.objects.get(shop_name=shop_name)

        site = feed.input_url
        hdr = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        feed_request = Request(site, headers=hdr)
        file = urllib.request.urlopen(feed_request)
        data = file.read()
        file.close()

        data = xmltodict.parse(data)
        items = data["rss"]["channel"]["item"]
        Serverkast_Product.objects.all().delete()
        print(json.dumps(items[0], indent=4))
        for item in items:
            if not ("gross_price" in item):
                print('item gross price is empty for')
                print(item["name"])
            else:
                Serverkast_Product.objects.create(
                    feed=feed,
                    is_selected=False,
                    sku=item["sku"],
                    name=item["name"],
                    short_desc=item.get("short_desc", "empty"),
                    long_description=item.get("long_description", "empty"),
                    main_image=item["main_image"],
                    extra_image_1=item.get("extra_image_1", None),
                    extra_image_2=item.get("extra_image_2", None),
                    extra_image_3=item.get("extra_image_3", None),
                    extra_image_4=item.get("extra_image_4", None),
                    extra_image_5=item.get("extra_image_5", None),
                    extra_image_6=item.get("extra_image_6", None),
                    extra_image_7=item.get("extra_image_7", None),
                    extra_image_8=item.get("extra_image_8", None),
                    extra_image_9=item.get("extra_image_9", None),
                    gross_price=item["gross_price"],
                    brand=item["brand"],
                    ean=item.get("ean", "empty"),
                    current_stock=item["current_stock"],
                    url_more_info=item["url_more_info"],
                    shipmentby=item.get("shipmentby", "unknown"),
                )

        """
            TODO-FFC
            SELECT JUST PRODUCT FROM CURRENT FEED
            FOR THIS SELECT THE PRODUCT MODEL DEPENDENT FROM shop_name PARAMETER
            CREATE OR REMOVE ALSO FINAL FEED PRODUCTS
        """
        feed = Feed.objects.get(shop_name=shop_name)
        products = Serverkast_Product.objects.all()
        template = get_template("product_selection_page.html")
        init = { row.name : row.is_selected for row in products }
        form = ProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "GET":
        feed = Feed.objects.get(shop_name=shop_name)
        products = Serverkast_Product.objects.all()
        template = get_template("product_selection_page.html")
        init = { row.name : row.is_selected for row in products }
        form = ProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
        }
        return HttpResponse(template.render(context, request))
