# Generated by Django 4.2.4 on 2023-11-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_coupon_coupon_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
