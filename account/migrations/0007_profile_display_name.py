# Generated by Django 3.2.4 on 2021-07-01 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_name',
            field=models.CharField(default='Anonymous', max_length=40),
        ),
    ]
