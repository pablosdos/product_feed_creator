# Generated by Django 4.2.6 on 2023-12-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0017_add_input_type_to_feed_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedconfiguration",
            name="original_fields_for_final_feed",
            field=models.CharField(
                default="", max_length=1023, verbose_name="Input Type"
            ),
            preserve_default=False,
        ),
    ]
