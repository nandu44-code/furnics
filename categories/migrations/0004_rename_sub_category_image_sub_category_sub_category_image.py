# Generated by Django 4.2.4 on 2023-09-13 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_sub_category_sub_category_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sub_category',
            old_name='Sub_Category_image',
            new_name='sub_Category_image',
        ),
    ]
