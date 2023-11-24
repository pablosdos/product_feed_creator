from django.template.loader import get_template
from django.http import HttpResponse
from product_feed_generator.models import Feed, Serverkast_Product
from django.contrib.auth.decorators import login_required

@login_required
def manage_product_import_view(request, shop_name):
    feeds = Feed.objects.all()
    context = {
        "feeds": feeds,
        "shop_name": shop_name,
    }
    template = get_template("manage_product_import_page.html")
    return HttpResponse(template.render(context, request))
