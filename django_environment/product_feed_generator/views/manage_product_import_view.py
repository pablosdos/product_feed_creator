from django.template.loader import get_template
from django.http import HttpResponse
from product_feed_generator.models import Feed, Serverkast_Product, TopSystemsProduct
from django.contrib.auth.decorators import login_required

@login_required
def manage_product_import_view(request, shop_name):
    if shop_name == "Serverkast":
        fields = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        fields = TopSystemsProduct._meta.fields[:]
    fieldsList = []
    for field in fields:
        fieldsList.append(field.name)
    fieldsList.pop(0)
    feeds = Feed.objects.all()
    context = {
        "feeds": feeds,
        "shop_name": shop_name,
        "fields": fieldsList,
    }
    template = get_template("manage_product_import_page.html")
    return HttpResponse(template.render(context, request))
