from django.template.loader import get_template
from django.http import HttpResponse
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
)
from django.contrib.auth.decorators import login_required

OPERATORS = [
    ("+", "+"),
    ("-", "-"),
    ("*", "*"),
    ("/", "/"),
    ("custom_value", "Custom Value – "),
]


@login_required
def manage_product_import_view(request, shop_name):
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    context = {}
    if "save-schema-config" in request.POST:
        selected_fields_for_final_feed = request.POST.get(
            "finalFeedProductSchemaStringInput", "[]"
        )
        original_fields_for_final_feed_1 = request.POST.get(
            "finalFeedProductSchemaStringInput1", "[]"
        )
        original_fields_for_final_feed_2 = request.POST.get(
            "finalFeedProductSchemaStringInput2", "[]"
        )
        FeedConfiguration.objects.filter(feed=feed_from_current_shop).update(
            product_schema_for_final_feed=selected_fields_for_final_feed
        )
        FeedConfiguration.objects.filter(feed=feed_from_current_shop).update(
            custom_calculated_field_1=original_fields_for_final_feed_1
        )
        FeedConfiguration.objects.filter(feed=feed_from_current_shop).update(
            custom_calculated_field_2=original_fields_for_final_feed_2
        )
        context.update({"update_message": "Schema updated!"}),
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).product_schema_for_final_feed
    custom_calc_field_1 = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_1
    custom_calc_field_2 = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_2
    # print(current_product_schema_for_final_feed)
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    availableFieldsList = []
    for field in allFieldsOfProduct:
        availableFieldsList.append(field.name)
    availableFieldsList.pop(0)
    # custom_calc_field = current_product_schema_for_final_feed.split(",")[0]
    custom_calc_field_name = custom_calc_field_1.split("-")[0]
    custom_calc_field_parts = custom_calc_field_1.split("-")[1:]
    custom_calc_field_name_2 = custom_calc_field_2.split("-")[0]
    custom_calc_field_parts_2 = custom_calc_field_2.split("-")[1:]
    finalFeedSchemaFieldsList = current_product_schema_for_final_feed.split(",")
    feeds = Feed.objects.all()
    context.update({"feeds": feeds}),
    context.update({"shop_name": shop_name}),
    context.update({"availableFields": availableFieldsList}),
    context.update(
        {"current_product_schema_for_final_feed": finalFeedSchemaFieldsList}
    ),
    context.update({"CustomCalcFieldName": custom_calc_field_name}),
    context.update({"CustomCalcFieldParts": custom_calc_field_parts}),
    context.update({"CustomCalcFieldName2": custom_calc_field_name_2}),
    context.update({"CustomCalcFieldParts2": custom_calc_field_parts_2}),
    context.update({"operators": OPERATORS}),
    # print(context)
    template = get_template("manage_product_import_page.html")
    return HttpResponse(template.render(context, request))
