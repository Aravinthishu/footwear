# Generated by Django 5.1.1 on 2024-10-01 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_desciption_herosection_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img1', models.ImageField(blank=True, null=True, upload_to='home_banner/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='home_banner/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='home_banner/')),
            ],
        ),
    ]
