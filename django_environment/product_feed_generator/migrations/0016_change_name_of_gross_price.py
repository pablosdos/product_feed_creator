# Generated by Django 4.2.6 on 2023-11-30 18:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0015_change_name_of_gross_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="finalfeedproduct",
            old_name="gross_price",
            new_name="sales_price_excluding_tax",
        ),
    ]
