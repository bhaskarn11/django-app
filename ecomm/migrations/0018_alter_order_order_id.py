# Generated by Django 3.2.4 on 2021-07-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0017_auto_20210702_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default='5e53811d4a0c46feb83f2d521b0bf871', unique=True),
        ),
    ]
