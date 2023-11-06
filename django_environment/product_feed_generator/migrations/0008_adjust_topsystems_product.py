# Generated by Django 4.2.6 on 2023-11-06 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0007_add_topsystems_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="topsystemsproduct",
            name="shipping_weight",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="topsystemsproduct",
            name="sku",
            field=models.CharField(max_length=63, verbose_name="MPN (originally SKU)"),
        ),
    ]
