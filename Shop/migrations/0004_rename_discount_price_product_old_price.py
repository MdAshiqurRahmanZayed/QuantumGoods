# Generated by Django 5.0 on 2024-01-06 16:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Shop", "0003_product_featured_product"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="discount_price",
            new_name="old_price",
        ),
    ]
