# Generated by Django 3.2.4 on 2021-10-04 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0033_auto_20211004_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, default='SKU087XIJN0HT', max_length=20),
        ),
    ]
