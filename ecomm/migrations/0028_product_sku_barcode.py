# Generated by Django 3.2.4 on 2021-09-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0027_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku_barcode',
            field=models.ImageField(default='products/barcode/default.jpg', upload_to='products'),
        ),
    ]
