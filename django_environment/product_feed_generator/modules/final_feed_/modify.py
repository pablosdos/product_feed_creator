import json
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
)


def _apply_configuration_scheme(selected_products_list, shop_name) -> list:
    """
    Receive a list of products.

    Returns configured list of products.
    """
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    # print(type(feed_from_current_shop))
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).product_schema_for_final_feed
    current_product_schema_for_final_feed = json.loads(
        current_product_schema_for_final_feed
    ).keys()
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    allOriginalAttributesOfList = []
    for field in allFieldsOfProduct:
        allOriginalAttributesOfList.append(field.name)
    attributes_to_remove_from_list = set(allOriginalAttributesOfList) - set(
        current_product_schema_for_final_feed
    )
    selected_products_list_with_custom_calc_field = _add_custom_calc_field(
        selected_products_list, allFieldsOfProduct, shop_name
    )

    for product in selected_products_list:
        for attribute_to_remove in attributes_to_remove_from_list:
            if attribute_to_remove in product:
                del product[attribute_to_remove]
    return selected_products_list_with_custom_calc_field


def _get_calculation_result(custom_field_with_name_and_parts) -> dict:
    """
    Receive elements for calculation as a list.

    Returns 1 calculated field as a dict.
    """
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
    # calculate the result value
    try:
        calc_result_value = eval(string_for_evaluation_in_python)
        return {
            "field_name": custom_calculated_field_1_name,
            "calc_result_value": calc_result_value,
        }
    except:
        return {
            "field_name": custom_calculated_field_1_name,
            "calc_result_value": "calculation invalid",
        }


def _add_custom_calc_field(
    selected_products_list, allFieldsOfProduct, shop_name
) -> list:
    """
    Recieve product list (list of dicts).

    Add every custom calc field (calculated value) of fitting configurations to the list.

    Returns updated product list (list of dicts).
    """
    #
    # TODO – implement
    # get calculation from conf of shop_name and calculate from allFieldsOfProduct
    # finally create and add the custom field to selected_products_list
    #
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    custom_calculated_field_1_name_and_parts = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_1.split("-")
    print(type(custom_calculated_field_1_name_and_parts))
    calc_result = _get_calculation_result(custom_calculated_field_1_name_and_parts)
    for product in selected_products_list:
        product.update({calc_result["field_name"]: calc_result["calc_result_value"]})
    custom_calculated_field_2_name_and_parts = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_2.split("-")
    calc_result = _get_calculation_result(custom_calculated_field_2_name_and_parts)
    for product in selected_products_list:
        product.update({calc_result["field_name"]: calc_result["calc_result_value"]})
    return selected_products_list
