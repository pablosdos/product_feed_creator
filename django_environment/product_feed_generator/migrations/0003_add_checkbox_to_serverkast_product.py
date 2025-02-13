# Generated by Django 4.2.6 on 2023-10-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0002_add_serverkast_product_and_feed_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="serverkast_product",
            name="is_selected",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="feed",
            name="input_url",
            field=models.URLField(max_length=511, verbose_name="XML URL"),
        ),
        migrations.AlterField(
            model_name="feed",
            name="shop_name",
            field=models.CharField(max_length=63, verbose_name="Shop Name"),
        ),
    ]
