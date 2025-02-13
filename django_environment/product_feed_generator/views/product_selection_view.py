from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import xmltodict
import urllib.request
from urllib.request import Request
import pprint
import json
from dicttoxml import dicttoxml
from product_feed_generator.models import Feed, FeedConfiguration, Serverkast_Product, TopSystemsProduct, IngramMicroProduct
from product_feed_generator.modules.final_feed_.base import FinalFeed_
from product_feed_generator.forms import *
from product_feed_generator.views.helper import *
from django.contrib.auth.decorators import login_required


@login_required
def product_selection_view(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    template = get_template("product_selection_page.html")
    """
    Configuration
    Form
    """
    initial = {
        "retail_price_excluding_tax_division_value": feed.feedconfiguration.retail_price_excluding_tax_division_value,
        "retail_price_excluding_tax_multiplication_value": feed.feedconfiguration.retail_price_excluding_tax_multiplication_value,
        "cost_price_multiplication_value": feed.feedconfiguration.cost_price_multiplication_value,
    }
    feed_config_form = FeedConfigForm(initial)
    """
    Toggle
    Auto
    Refresh
    """
    if "toggle_auto_refresh_submit" in request.POST:
        Feed.objects.filter(shop_name=shop_name).update(
            products_update_cronjob_active=not feed.products_update_cronjob_active
        )
        feed = Feed.objects.get(shop_name=shop_name)
        if shop_name == "Serverkast":
            current_products = Serverkast_Product.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = ServerkastProductSelectForFinalFeedForm(init)
        elif shop_name == "TopSystems":
            current_products = TopSystemsProduct.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = TopSystemsProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
            "feed_config_form": feed_config_form,
        }
        return HttpResponse(template.render(context, request))

    elif "toggle_auto_add_new_products" in request.POST:
        Feed.objects.filter(shop_name=shop_name).update(
            auto_add_new_products_cronjob_active=not feed.auto_add_new_products_cronjob_active
        )
        feed = Feed.objects.get(shop_name=shop_name)
        if shop_name == "Serverkast":
            current_products = Serverkast_Product.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = ServerkastProductSelectForFinalFeedForm(init)
        elif shop_name == "TopSystems":
            current_products = TopSystemsProduct.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = TopSystemsProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
            "feed_config_form": feed_config_form,
        }
        return HttpResponse(template.render(context, request))

    elif "add_products_to_final_feed_submit" in request.POST:
        finalfeed = FinalFeed_(shop_name)
        # topsystems_finalfeed._apply_configuration_scheme(complete_topsystems_products_list)
        context = finalfeed.save_xml_file(request)
        # print(type(context))
        del finalfeed
        return HttpResponse(template.render(context, request))

    elif "generate_refresh_submit" in request.POST:
        context = extract_and_save_products(request, shop_name)
        return HttpResponse(template.render(context, request))

    elif "generate_refresh_submit_with_password" in request.POST:
        current_products = IngramMicroProduct.objects.all()
        init = {
            "%s ––– %s" % (row.ean, row.ingram_part_description): row.is_selected
            for row in current_products
        }
        form = IngramMicroProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
        }
        try:
            context = extract_and_save_products_with_password(request, shop_name)
        except:
            """
            Error
            If
            Credentials
            Wrong
            """
            context.update({"note": "Protection Credentials not known or incorrect"}),
            return HttpResponse(template.render(context, request))
        return HttpResponse(template.render(context, request))

    elif "submit_config_update" in request.POST:
        feedconfig = FeedConfiguration.objects.filter(feed=feed)
        FeedConfiguration.objects.filter(feed=feed).update(
            retail_price_excluding_tax_division_value=request.POST.get("retail_price_excluding_tax_division_value", 0.0),
            retail_price_excluding_tax_multiplication_value=request.POST.get("retail_price_excluding_tax_multiplication_value", 0.0),
            cost_price_multiplication_value=request.POST.get("cost_price_multiplication_value", 0.0),
        )
        # FeedConfiguration.objects.filter(feed=feed).update(
        #     retail_price_excluding_tax_division_value=request.POST['retail_price_excluding_tax_division_value'],
        #     retail_price_excluding_tax_multiplication_value=request.POST['retail_price_excluding_tax_multiplication_value'],
        #     cost_price_multiplication_value=request.POST['cost_price_multiplication_value']
        # )
        feed = Feed.objects.get(shop_name=shop_name)
        initial = {
            "retail_price_excluding_tax_division_value": feed.feedconfiguration.retail_price_excluding_tax_division_value,
            "retail_price_excluding_tax_multiplication_value": feed.feedconfiguration.retail_price_excluding_tax_multiplication_value,
            "cost_price_multiplication_value": feed.feedconfiguration.cost_price_multiplication_value,
        }
        if shop_name == "Serverkast":
            current_products = Serverkast_Product.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = ServerkastProductSelectForFinalFeedForm(init)
        elif shop_name == "TopSystems":
            current_products = TopSystemsProduct.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = TopSystemsProductSelectForFinalFeedForm(init)
        feed_config_form = FeedConfigForm(initial)
        context = {
            "feed": feed,
            "form": form,
            "feed_config_form": feed_config_form,
        }
        return HttpResponse(template.render(context, request))

    elif request.method == "GET":
        """
        GET
        REQUEST
        OF PAGE
        Product
        Selection
        Form
        """
        if shop_name == "Serverkast":
            current_products = Serverkast_Product.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = ServerkastProductSelectForFinalFeedForm(init)
        elif shop_name == "TopSystems":
            current_products = TopSystemsProduct.objects.all()
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.name): row.is_selected
                for row in current_products
            }
            form = TopSystemsProductSelectForFinalFeedForm(init)
        elif shop_name == "IngramMicro":
            """
            TODO – IMPLEMENT PAGINATION
            FOR DEMO JUST FIRST 1000 PRODUCTS
            """
            current_products = IngramMicroProduct.objects.all()[0:1000]
            # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
            init = {
                "%s ––– %s" % (row.ean, row.ingram_part_description): row.is_selected
                for row in current_products
            }
            form = IngramMicroProductSelectForFinalFeedForm(init)
        context = {
            "feed": feed,
            "form": form,
            # "feed_config_form": feed_config_form,
        }
        return HttpResponse(template.render(context, request))
