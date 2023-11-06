from django.db import models

class Feed(models.Model):
    shop_name = models.CharField(max_length=63, verbose_name='Shop Name')
    input_url = models.URLField(max_length=511, verbose_name='XML URL')
    products_last_updated = models.DateTimeField()
    products_update_cronjob_active = models.BooleanField()

    def __str__(self):
        return f"{self.shop_name}"