# Generated by Django 4.2.6 on 2023-11-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0009_adjust_topsystems_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="feed",
            name="products_last_updated",
            field=models.DateField(default="2022-12-27"),
            preserve_default=False,
        ),
    ]
