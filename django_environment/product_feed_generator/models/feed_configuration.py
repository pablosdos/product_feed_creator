from django.db import models
from product_feed_generator.models import Feed

class FeedConfiguration(models.Model):
    feed = models.OneToOneField(
        Feed,
        on_delete=models.CASCADE,
    )
    retail_price_excluding_tax_division_value = models.DecimalField(max_digits=9, decimal_places=2)
    retail_price_excluding_tax_multiplication_value = models.DecimalField(max_digits=9, decimal_places=2)
    cost_price_multiplication_value = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.feed} Configuration"
