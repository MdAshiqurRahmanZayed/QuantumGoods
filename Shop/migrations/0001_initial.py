# Generated by Django 5.0 on 2024-04-14 17:32

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, max_length=300)),
                (
                    "cat_image",
                    models.ImageField(blank=True, upload_to="images/categories"),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=50, unique=True)),
                (
                    "discount_percentage",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(100),
                            django.core.validators.MinValueValidator(1),
                        ],
                    ),
                ),
                (
                    "cupon_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=200, unique=True)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=200, null=True, unique=True
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=500)),
                ("price", models.IntegerField()),
                ("images", models.ImageField(upload_to="images/products")),
                ("stock", models.IntegerField()),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("featured_product", models.BooleanField(default=False)),
                ("old_price", models.IntegerField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Shop.category"
                    ),
                ),
                (
                    "coupon_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Shop.coupon",
                    ),
                ),
                (
                    "product_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductGallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(max_length=255, upload_to="images/products"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Shop.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "productgallery",
                "verbose_name_plural": "product gallery",
            },
        ),
        migrations.CreateModel(
            name="ReviewRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(blank=True, max_length=100)),
                ("review", models.TextField(blank=True, max_length=500)),
                ("rating", models.FloatField()),
                ("ip", models.CharField(blank=True, max_length=20)),
                ("status", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Shop.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Variation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "variation_category",
                    models.CharField(
                        choices=[("color", "color"), ("size", "size")], max_length=100
                    ),
                ),
                ("variation_value", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Shop.product"
                    ),
                ),
            ],
        ),
    ]
