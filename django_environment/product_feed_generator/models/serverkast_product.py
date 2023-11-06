from django.db import models

class Serverkast_Product(models.Model):
    # one of many Serverkast_Products for one Feed | if Feed is deleted, Serverkast_Products from this Feed as well
    feed = models.ForeignKey(
        "Feed", on_delete=models.CASCADE, blank=False, null=False
    )
    is_selected = models.BooleanField()
    sku = models.CharField(max_length=63)
    name = models.CharField(max_length=127)
    short_desc = models.CharField(max_length=127)
    long_description = models.CharField(max_length=2055)
    main_image = models.URLField(max_length=511, null=True, blank=True)
    extra_image_1 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_2 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_3 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_4 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_5 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_6 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_7 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_8 = models.URLField(max_length=511, null=True, blank=True)
    extra_image_9 = models.URLField(max_length=511, null=True, blank=True)
    gross_price = models.DecimalField(max_digits=9, decimal_places=2)
    brand = models.CharField(max_length=63)
    ean = models.CharField(max_length=63)
    current_stock = models.CharField(max_length=63)
    url_more_info = models.URLField(max_length=511)
    shipmentby = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.name}"