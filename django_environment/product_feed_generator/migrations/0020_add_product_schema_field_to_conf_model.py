# Generated by Django 4.2.6 on 2023-12-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0019_add_custom_calc_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedconfiguration",
            name="product_schema_for_final_feed",
            field=models.CharField(
                default="",
                max_length=1023,
                verbose_name="Product Schema For Final Field",
            ),
            preserve_default=False,
        ),
    ]
