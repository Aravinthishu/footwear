# Generated by Django 5.1.1 on 2024-09-28 10:48

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('small_description', tinymce.models.HTMLField(blank=True, null=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('normal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('final_price', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('stock', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='products/')),
                ('extra_images', models.ImageField(blank=True, null=True, upload_to='products/extra/')),
                ('extra_image_2', models.ImageField(blank=True, null=True, upload_to='products/extra/')),
                ('extra_image_3', models.ImageField(blank=True, null=True, upload_to='products/extra/')),
                ('extra_image_4', models.ImageField(blank=True, null=True, upload_to='products/extra/')),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='category.maincategory')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='category.subcategory')),
                ('super_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='category.supercategory')),
                ('sizes', models.ManyToManyField(related_name='products', to='product.size')),
            ],
        ),
    ]
