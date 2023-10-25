from django.db import models

class Feed(models.Model):
    shop_name = models.CharField(max_length=63, verbose_name='Shop Name')
    input_url = models.URLField(max_length=511, verbose_name='XML URL')

    def __str__(self):
        return f"{self.shop_name}"