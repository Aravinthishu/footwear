# Generated by Django 5.1.1 on 2024-10-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_herosection_button_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herosection',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='homebanner',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='homebanner',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='homebanner',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='homebanner2',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
