from django.template.loader import get_template
from django.http import HttpResponse
import json
from product_feed_generator.forms import *
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
    IngramMicroProduct,
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
    """
    Default
    dynamic
    configuration
    page data
    added to
    context
    """
    request_post_body = request.POST
    context = {}
    feeds = Feed.objects.all()
    feed_from_current_shop_for_filtering = Feed.objects.get(shop_name=shop_name)
    feed_conf_from_current_shop = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    )
    feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
        feed=feed_from_current_shop_for_filtering
    )
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    ).product_schema_for_final_feed
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    elif shop_name == "IngramMicro":
        allFieldsOfProduct = IngramMicroProduct._meta.fields[:]
    availableFieldsList = []
    for field in allFieldsOfProduct:
        availableFieldsList.append(field.name)
    availableFieldsList.pop(0)
    if current_product_schema_for_final_feed == []:
        finalFeedSchemaFieldsList = []
    else:
        finalFeedSchemaFieldsList = json.loads(
            current_product_schema_for_final_feed
        ).keys()
    custom_calculation_units_list = json.loads(
        feed_conf_from_current_shop.custom_calculation_units_list
    )
    context.update({"CustomCalcUnits": custom_calculation_units_list}),
    context.update({"feeds": feeds}),
    context.update({"shop_name": shop_name}),
    context.update({"availableFields": availableFieldsList}),
    context.update(
        {"current_product_schema_for_final_feed": finalFeedSchemaFieldsList}
    ),
    context.update({"operators": OPERATORS}),
    template = get_template("manage_product_import_page.html")
    # provide for IngramMicro additionally credentials_form
    initial = {
        "xml_user": feed_conf_from_current_shop.xml_user,
        "xml_pass": feed_conf_from_current_shop.xml_pass,
        "sftp_url": feed_conf_from_current_shop.sftp_url,
    }
    credentials_form = SftpXmlCredentialsForm(initial)
    context.update({"credentials_form": credentials_form}),
    # adding custom calc field
    if "add_custom_calc_field" in request.GET:
        json_ = {
            "custom_calc_field_name": "",
            "calculation_elements": [],
        }
        custom_calculation_units_list.append(json_)
        custom_calculation_units_list_as_json_for_database = json.dumps(custom_calculation_units_list)
        feed_conf_from_current_shop_for_updating.update(
            custom_calculation_units_list=custom_calculation_units_list_as_json_for_database
        )
        context.update({"CustomCalcUnits": custom_calculation_units_list})
    # save-protection-credentials
    if "save-protection-credentials" in request_post_body:
        # print(request_post_body.get("xml_pass", ""))
        feed_conf_from_current_shop_for_updating.update(
            xml_user=request_post_body.get("xml_user", "")
        )
        feed_conf_from_current_shop_for_updating.update(
            xml_pass=request_post_body.get("xml_pass", "")
        )
        feed_conf_from_current_shop_for_updating.update(
            sftp_url=request_post_body.get("sftp_url", "")
        )
        context.update({"update_message": "Protection credentials updated!"}),
    """
    Add changed
    configurations
    to database
    """
    if "save-schema-config" in request_post_body:
        # print(request_post_body)
        feed_conf_from_current_shop_for_updating.update(
            product_schema_for_final_feed=request_post_body.get(
                "finalFeedProductSchemaWithoutCustomCalcUnits", "[]"
            )
        )

        context.update({"update_message": "Schema updated!"}),

    return HttpResponse(template.render(context, request))
