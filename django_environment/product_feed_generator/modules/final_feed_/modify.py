import copy
import json
from decimal import Decimal
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
)
# from .add_custom_calc_field import *

def _apply_configuration_scheme(selected_products_list, shop_name):
    # print(selected_products_list)
    #1 find attributes to remove
    #filter list
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    # current_product_schema_for_final_feed = FeedConfiguration.objects.get(
    #     feed=feed_from_current_shop
    # ).product_schema_for_final_feed.split(",")
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).product_schema_for_final_feed
    current_product_schema_for_final_feed = json.loads(current_product_schema_for_final_feed).keys()

    
    #original attributes list
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    allOriginalAttributesOfList = []
    for field in allFieldsOfProduct:
        allOriginalAttributesOfList.append(field.name)
    attributes_to_remove_from_list = set(allOriginalAttributesOfList) - set(current_product_schema_for_final_feed)
    #2 clean products by filter list
    # print(attributes_to_remove_from_list)
    selected_products_list_with_custom_calc_field = _add_custom_calc_field(selected_products_list, allFieldsOfProduct, shop_name)
    # print(selected_products_list_with_custom_calc_field)

    for product in selected_products_list:
        for attribute_to_remove in attributes_to_remove_from_list:
            if attribute_to_remove in product:
                del product[attribute_to_remove]
    
    return selected_products_list_with_custom_calc_field

def _get_calculation_result(custom_field_with_name_and_parts):
    custom_calculated_field_1_name = custom_field_with_name_and_parts[0]
    custom_calculated_field_1_parts = custom_field_with_name_and_parts[1:]
    string_for_evaluation_in_python = ""
    for part in custom_calculated_field_1_parts:
        if any(ext in part for ext in ["+", "-", "*", "/"]):
            string_for_evaluation_in_python = string_for_evaluation_in_python + part
        elif "custom_value_" in part:
            string_for_evaluation_in_python = (
                string_for_evaluation_in_python
                + "Decimal("
                + part.split("custom_value_")[1]
                + ")"
            )
        else:
            string_for_evaluation_in_python = (
                string_for_evaluation_in_python + "product.get('" + part + "')"
            )
    string_for_evaluation_in_python = "round(" + string_for_evaluation_in_python + ",2)"
    # print(string_for_evaluation_in_python)
    return {"field_name": custom_calculated_field_1_name, "eval_string": string_for_evaluation_in_python}


def _add_custom_calc_field(selected_products_list, allFieldsOfProduct, shop_name):
    #
    # TODO – implement
    # get calculation from conf of shop_name and calculate from allFieldsOfProduct
    # finally create and add the custom field to selected_products_list
    #
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    # CUSTOM CALC FIELD 1
    custom_calculated_field_1_name_and_parts = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_1.split("-")
    calc_result = _get_calculation_result(custom_calculated_field_1_name_and_parts)
    # print(calc_result)
    for product in selected_products_list:
        try:
            product.update(
                {calc_result['field_name']: eval(calc_result['eval_string'])}
            )
        except:
            product.update({calc_result['field_name']: "calculation_invalid"})
            # print('not working')
    # CUSTOM CALC FIELD 2
    custom_calculated_field_2_name_and_parts = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_2.split("-")
    calc_result = _get_calculation_result(custom_calculated_field_2_name_and_parts)
    for product in selected_products_list:
        try:
            product.update(
                {calc_result['field_name']: eval(calc_result['eval_string'])}
            )
        except:
            product.update({calc_result['field_name']: "calculation_invalid"})
            # print('not working')
    return selected_products_list
