# Generated by Django 4.2.4 on 2023-10-06 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_variation_images_variantimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='images',
            field=models.ImageField(default=None, upload_to='photos/products/'),
        ),
    ]
