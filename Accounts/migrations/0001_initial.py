# Generated by Django 5.0 on 2024-05-21 09:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=50, unique=True)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now_add=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("is_superadmin", models.BooleanField(default=False)),
                (
                    "user_type",
                    models.CharField(
                        choices=[("buyer", "Buyer"), ("seller", "Seller")],
                        default="buyer",
                        max_length=20,
                        verbose_name="User Type",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "address_line_1",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        default="default/user.png",
                        null=True,
                        upload_to="images/profile",
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=20, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=20, null=True)),
                ("country", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
